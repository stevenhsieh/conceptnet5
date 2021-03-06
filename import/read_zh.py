from conceptnet.models import Frame
from conceptnet5.graph import JSONWriterGraph, ConceptNetGraph
import os
import codecs

GRAPH = JSONWriterGraph('json_data/zh')
#GRAPH = ConceptNetGraph('localhost:7474')

def handle_file(filename):
    petgame = GRAPH.get_or_create_node(u'/source/activity/petgame')
    GRAPH.justify(0, petgame)

    for line in codecs.open(filename, encoding='utf-8', errors='replace'):
        line = line.strip()
        if line:
            parts = line.split(', ')
            user, frame_id, concept1, concept2 = parts
            frame = Frame.objects.get(id=int(frame_id))
            relation = frame.relation
            assertion = GRAPH.get_or_create_assertion(
                '/relation/'+relation.name,
                [u'/concept/zh_TW/'+concept1, u'/concept/zh_TW/'+concept2],
                {'dataset': 'conceptnet/zh_TW', 'license': 'CC-By'}
            )

            raw = GRAPH.get_or_create_assertion(
                '/frame/zh_TW/'+frame.text,
                [u'/concept/zh_TW/'+concept1, u'/concept/zh_TW/'+concept2],
                {'dataset': 'conceptnet/zh_TW', 'license': 'CC-By'}
            )

            source_uri = u"/source/contributor/petgame/%s" % user
            source = GRAPH.get_or_create_node(source_uri)
            GRAPH.justify(0, source, weight=0.5)
            
            conjunction = GRAPH.get_or_create_conjunction([source, petgame])
            raw, norm = GRAPH.make_assertion_pair(
                (GRAPH.make_frame('zh_TW', frame.text),
                 GRAPH.make_concept('zh_TW', concept1),
                 GRAPH.make_concept('zh_TW', concept2)
                ),
                (GRAPH.make_relation(relation.name),
                 GRAPH.make_concept('zh_TW', concept1),
                 GRAPH.make_concept('zh_TW', concept2)
                ),
                dataset='conceptnet/zh_TW',
                license='CC-By',
            )

            GRAPH.justify(conjunction, raw)
            print norm

if __name__ == '__main__':
    for filename in os.listdir('.'):
        if filename.startswith('conceptnet_zh_'):
            handle_file(filename)


from __future__ import print_function,unicode_literals
import json
from relation_functions import extract_entity


def index1(doc,label1, label2, scope = 1):
    sent_index = {}
    sent_order = {}
    lower_label1 = str(label1.lower())
    lower_label2 = str(label2.lower())
    for index,sent in enumerate(doc.sents):
        sent_index[sent] = index
    for index,sent in enumerate(doc.sents):
        sent_order[index] = sent
    entities = []
    types = [lower_label1, lower_label2]
    for ent2 in doc.user_data[label2]:
        for ent1 in doc.user_data[label1]:
            obj = dict()
            ent1_sent = ent1.sent
            ent2_sent = ent2.sent

            ent1_sent_i = sent_index[ent1_sent]
            ent2_sent_i = sent_index[ent2_sent]
            if abs(ent1_sent_i - ent2_sent_i) < scope:
                obj[str("entities")] = types
                obj[lower_label1] = {
                                str("value"): ent1._.text,
                                str("position"):  ent1.sent.text.index(ent1._.text),
                                str("length"): len(ent1._.text),
                                str("type"): lower_label1
                                }
                obj[lower_label2] =  {
                                str("value"): ent2._.text,
                                str("position"):  ent2.sent.text.index(ent2._.text),
                                str("length"): len(ent2._.text),
                                str("index"): ent2.i,
                                str("type"):lower_label2
                                }
                sentence1 = ent1.sent
                sentence2 = ent2.sent
                low = ent1_sent_i if ent1_sent_i < ent2_sent_i  else ent2_sent_i
                high = ent1_sent_i if ent1_sent_i > ent2_sent_i  else ent2_sent_i
                phrase_list = " ".join([sent.text for sent in list(doc.sents)[low:high+1]])
                phrase_ = "".join(phrase_list)
                obj[str("phrase")] = {
                                    str("text"): str(phrase_list)
                                        }
                obj[str("sentence1")] = {
                                    str("text"): str(sentence1),
                                    str("index"): sent_index[sentence1]
                                    }
                obj[str("sentence2")] = {
                                    str("text"): str(sentence2),
                                    str("index"): sent_index[sentence2]
                }
                obj[str("relation")] = {
                                    str("text"): [str(anc) for anc in ent2.ancestors if anc.pos_ in ["VERB", "NOUN"]],
                                    str("POS"): [anc.pos_ for anc in ent2.ancestors]
                                    }
                obj[str("relation1")] = {
                                    str("text"): [str(anc) for anc in ent1.ancestors if anc.pos_ in ["VERB", "NOUN"]]
                                    }
                obj[str("children")] = {
                                    str("text"): [[str(child) for child in anc.children] for anc in ent2.ancestors ]
                                    }
                entities.append(obj)
    return entities
def index2(doc,label1, relation, scope = 1):
    sent_index = {}
    sent_order = {}
    lower_label = str(label1.lower())
    lower_relation = str(relation.lower())
    for index,sent in enumerate(doc.sents):
        sent_index[sent] = index
    for index,sent in enumerate(doc.sents):
        sent_order[index] = sent
    entities = []
    types = [lower_label, lower_relation]
    for ent1 in doc.user_data[label1]:
        for rel in doc.user_data[relation]:
            obj = dict()
            ent1_sent = ent1.sent
            rel_sent = rel.sent
            ent1_sent_i = sent_index[ent1_sent]
            rel_sent_i = sent_index[rel_sent]
            if abs(ent1_sent_i - rel_sent_i) < scope:
                obj[str("entities")] = types
                obj[lower_label] = {
                                str("value"): ent1._.text,
                                str("position"):  ent1.sent.text.index(ent1._.text),
                                str("length"): len(ent1._.text),
                                str("type"): lower_label
                                }
                obj[lower_relation] =  {
                                str("value"): rel.text,
                                str("position"):  rel.sent.text.index(rel.text),
                                str("length"): len(rel.text),
                                str("index"): rel.i,
                                str("type"):lower_relation
                                }
                sentence1 = ent1.sent
                sentence2 = rel.sent
                ent_token = rel
                entity = extract_entity(ent_token, relation)
                if entity:
                    obj[str("entity")] = {
                                        str("value"): str(entity.text),
                                        str("position"): entity.sent.text.index(entity.text),
                                        str("length"): len(entity.text),
                                        str("index"): entity.i,
                                        str("sentence"): str(entity.sent),
                                        }
                low = ent1_sent_i if ent1_sent_i < rel_sent_i  else rel_sent_i
                high = ent1_sent_i if ent1_sent_i > rel_sent_i  else rel_sent_i

                phrase_list = [sent.text for sent in list(doc.sents)[low:high+1]]
                phrase_ = " ".join(phrase_list)
                obj[str("phrase")] = {
                                    str("text"): str(phrase_)
                                        }
                obj[str("sentence1")] = {
                                    str("text"): str(sentence1),
                                    str("index"): sent_index[sentence1]
                                    }
                obj[str("sentence2")] = {
                                    str("text"): str(sentence2),
                                    str("index"): sent_index[sentence2]
                }
                obj[str("relation")] = {
                                    str("text"): [str(anc) for anc in rel.ancestors],
                                    str("POS"): [anc.pos_ for anc in rel.ancestors]
                                    }
                obj[str("relation1")] = {
                                    str("text"): [str(anc) for anc in ent1.ancestors]
                                    }
                obj[str("children")] = {
                                    str("text"): [[str(child) for child in anc.children] for anc in rel.ancestors]
                                    }
                entities.append(obj)
    return entities

def index3(doc,label1, label2,relation,scope = 1):
    sent_index = {}
    sent_order = {}
    lower_label1 = str(label1.lower())
    lower_label2 = str(label2.lower())
    rel_label = str(relation.lower())
    for index,sent in enumerate(doc.sents):
        sent_index[sent] = index
    for index,sent in enumerate(doc.sents):
        sent_order[index] = sent
    entities = []
    types = [lower_label1, lower_label2]
    for ent2 in doc.user_data[label2]:
        for ent1 in doc.user_data[label1]:
            obj = dict()
            ent1_sent = ent1.sent
            ent2_sent = ent2.sent
            ent1_sent_i = sent_index[ent1_sent]
            ent2_sent_i = sent_index[ent2_sent]
            if abs(ent1_sent_i - ent2_sent_i) < scope:
                obj[str("entities")] = types
                obj[lower_label1] = {
                                str("value"): ent1._.text,
                                str("position"):  ent1.sent.text.index(ent1._.text),
                                str("length"): len(ent1._.text),
                                str("type"): lower_label1
                                }
                obj[lower_label2] =  {
                                str("value"): ent2._.text,
                                str("position"):  ent2.sent.text.index(ent2._.text),
                                str("length"): len(ent2._.text),
                                str("index"): ent2.i,
                                str("type"):lower_label2
                                }
                sentence1 = ent1.sent
                sentence2 = ent2.sent
                low = ent1_sent_i if ent1_sent_i < ent2_sent_i  else ent2_sent_i
                high = ent1_sent_i if ent1_sent_i > ent2_sent_i  else ent2_sent_i
                phrase_list = [sent.text for sent in list(doc.sents)[low:high+1]]
                for rel in doc.user_data[relation]:
                    if rel.sent.text in phrase_list:
                        rel_entity = rel
                        obj[str(relation)] = {
                                            str("value"): str(rel_entity.text),
                                            str("position"): rel_entity.sent.text.index(rel_entity.text),
                                            str("length"): len(rel_entity.text),
                                            str("index"): rel_entity.i,
                                            str("sentence"): str(rel_entity.sent),
                                            str("type"): rel_label
                                            }
                        obj[str("relation")] = {
                                                str("value"): str(rel_label)
                                                }
                        break
                phrase_ = "".join(phrase_list)
                obj[str("phrase")] = {
                                    str("text"): str(phrase_list)
                                        }
                obj[str("sentence1")] = {
                                    str("text"): str(sentence1),
                                    str("index"): sent_index[sentence1]
                                    }
                obj[str("sentence2")] = {
                                    str("text"): str(sentence2),
                                    str("index"): sent_index[sentence2]
                }
                entities.append(obj)
    return entities
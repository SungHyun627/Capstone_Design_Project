import json
import firebase_admin
from firebase_admin import credentials, firestore
from google.cloud import dialogflow
import threading
import time
import pprint # 이거 추가 
from urllib.parse import unquote

cred = None
db = None
transaction = None
def initialize():
    cred = credentials.Certificate("/home/pi/PiReader/src/apibucket/pi-reader-qt99-firebase-adminsdk-pjfom-846fa09d75.json")
    firebase_admin.initialize_app(cred)

    # DB connection
    db = firestore.client()

    # DB transaction
    transaction = db.transaction()

    # DB status field
    # db_status_ref = db.collection(u'pi').document(u'status')
    print('is it called multiple time?')
    # Create an Event for notifying main thread.
    # ###### Control functions ###########
    return db,transaction

@firestore.transactional
def find_control_update(transaction, command):
    Word.get(command)
    definition = Word.definitions()
    print(definition)

    
@firestore.transactional
def picture_control_update(transaction):
    transaction.update(db.collection(u'pi').document(u'status'), {
        u'picture': True
     })
    # ########### False로 바꿔야 할 때 설정 필요 #####

@firestore.transactional
def reading_control_update(db, transaction, command):
    if command == "stop":
        transaction.update(db.collection(u'pi').document(u'status'), {
            u'play': False
        })
    else:
        transaction.update(db.collection(u'pi').document(u'status'), {
            u'play': True
        })

@firestore.transactional
def speed_volume_update(db, transaction, command, value, field):
    if command == "decrease":
        value = -value
    snapshot = db.collection(u'pi').document(u'status').get(transaction=transaction)
    if field == "speed":
        new_value = snapshot.get(u'speed') + value
    else:
        new_value = snapshot.get(u'volume') + value
    
    if new_value >= 10:
        new_value = 10
    else:
        if new_value < 1:
            new_value = 1
    
    if field == "speed":
        transaction.update(db.collection(u'pi').document(u'status'), {
            u'speed': new_value
        })
    else : 
        transaction.update(db.collection(u'pi').document(u'status'), {
        u'volume': new_value
    })
    
@firestore.transactional
def move_control_update(db, transaction, command, value):
    if command == "before":
        value = -value
    transaction.update(db.collection(u'pi').document(u'status'), {
        u'move_num': value,
        u'move': True
    })

    # ######### Move를 false로 바꿔야 할 때 설정 필요 ########

@firestore.transactional
def mark_make_update(transaction, db,command):
    snapshot = db.collection(u'pi').document(u'status').get(transaction=transaction)
    mark_index_list = snapshot.get(u'mark_index')
    mark_index_num_list = snapshot.get(u'mark_index_num')
    # 해당 북마크가 없을 때
    if command not in mark_index_list:
        mark_index_list.append(command)
        mark_index_num_list.append(0)
        transaction.update(db.collection(u'pi').document(u'status'), {
            u'mark_index' : mark_index_list,
            u'mark_index_num': mark_index_num_list
        })
        data = {
            u'text' : [0]
        }
        db.collection(u'bookmark').document(u'{}'.format(command)).set(data)
    else:
        # 해당 카테고리가 있을 때
        return "The category already exists"

@firestore.transactional
def mark_save_update(transaction, db,command, input_text):
    snapshot = db.collection(u'pi').document(u'status').get(transaction=transaction) 
    bookmark_snapshot = db.collection(u'bookmark').document(u'{}'.format(command)).get(transaction=transaction)
    mark_index_list = snapshot.get(u'mark_index')
    mark_index_num_list = snapshot.get(u'mark_index_num')

    # 해당 카테고리가 있을 때
    if command in mark_index_list:
        mark_index_num_list[mark_index_list.index(command)] += 1
        transaction.update(db.collection(u'pi').document(u'status'), {
            u'mark_index_num': mark_index_num_list,
            # ########### False로 바꿔야 할 때 설정 필요 #####
            u'mark_save': True,
            u'mark_save_category': command
        })

        mark_list = bookmark_snapshot.get(u'text')
        mark_list[0] += 1
        # bookmark할 문서 삽입
        mark_list.append(input_text)
        transaction.update(db.collection(u'bookmark').document(u'{}'.format(command)), {
            u'text' : mark_list
        })
    else:
        # 해당 카테고리가 없을 때
        return "There is no matching category"

@firestore.transactional
def mark_call_update(transaction,db, command, value):
    snapshot = db.collection(u'pi').document(u'status').get(transaction=transaction) 
    bookmark_snapshot = db.collection(u'bookmark').document(u'{}'.format(command)).get(transaction=transaction)
    mark_index_list = snapshot.get(u'mark_index')
    mark_index_num_list = snapshot.get(u'mark_index_num')

    # 해당 카테고리가 있을 때
    if command in mark_index_list:
        if mark_index_num_list[mark_index_list.index(command)] > value:
            transaction.update(db.collection(u'pi').document(u'status'), {
                u'mark_call_num': value,
                # ########### False로 바꿔야 할 때 설정 필요 #####
                u'mark_call': True,
                u'mark_call_category': command
            })
            mark_list = bookmark_snapshot.get(u'text')
            called_mark_list = mark_list[value:]
            print(called_mark_list)
            return called_mark_list
        else:
            # Index 범위를 벗어날 때
            return "Index out of range"
    else:
        return "There is no matching category"

def command_for_response(fulfillment_text):
    if "?" in fulfillment_text:
        addition_text = input("추가 질문 {} : \n".format(fulfillment_text))
        if "to which" in fulfillment_text:
            addition_text = "save to" + addition_text
        elif "which word" in funfillment_text:
            addition_text = "find" + addition_text
        else:
            addition_text = "build category as " + addition_text
        return addition_text



# doc_watch= db.collection(u'pi').document(u'status').on_snapshot(on_snapshot)
if __name__ == '__main__':
    while True: 
        text = input("입력 : ")

# self.project_id = 'pi-reader-qt99'
# self.session_id = 'Pi_Reader'
# self.audio_file = 'dialog2.wav'
# self.language_code = 'en'



# while True:
#     time.sleep(1)
#     print("processing...")
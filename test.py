from fastapi import FastAPI,HTTPException
from pydantic import BaseModel
import bcrypt,uuid
import json,os.path
from datetime import datetime as dt , time as t
from summer import summer

# tstamp_today : int  = int(dt.combine(dt.now(pytz.timezone('Asia/Calcutta')),t.min).timestamp())

tstamp_today : int = int(dt(dt.now().year,dt.now().month,dt.now().day,00,00,00).timestamp())

PATHS : tuple = ('database/users_data.json','database/journal_data.json')
PATH_TEMP_DATAS : tuple = {
    PATHS[0] : {
    '123' : {
        'email' : '123@gmail.com',
        'dob' : 976579200000,
        'id': '3cc4505f-3678-414c-b544-e26555728b9c',
        'password': '$2b$12$buI43Y8ggvWzgTyqlLoBxupe/ojPEEKbV/mAofu7pCs/JGQWqn.9G'
    }
},
    PATHS[1] : {
        '3cc4505f-3678-414c-b544-e26555728b9c':{
        tstamp_today : {
        'completed' : [],
        'not_completed' : [],
        'mood' : 0,
        'productivity' : 0,
        'stress_level' : 0,
        'social_interaction' : 0,
        'energy_level': 0,
        'lessons' : '',
        'thankful' : [],
        'sucks' : ''    
        },
    }
}
}


app = FastAPI()
# uvicorn test:app --reload
# tasklist /FI "IMAGENAME eq python.exe" <---- KILL CMD for uvicorn 
#taskkill /PID <PID> /F

def check_file_exists() -> None:
    count : int = 0
    for path in PATHS:
        if not os.path.exists(path):        
            try:
                with open(path,"w") as outfile:
                    json.dump(PATH_TEMP_DATAS[path],outfile,indent=10)                        
            except Exception as e:
                print(f'Error: {e}')
        else:
            try: 
                with open(path,"r") as outfile:
                    outfile.seek(0, os.SEEK_END)
                    file_size = outfile.tell()
                    if (file_size == 0):
                        with open(path,"w") as outfile:
                            json.dump(PATH_TEMP_DATAS[path],outfile,indent=10)  
            except Exception as e:
                print(f'Error: {e}')
            finally:
                count+=1
    print(f"\nFound:{count}/{len(PATHS)}")
    if count != len(PATHS):
        check_file_exists()

def retrive_data(path) -> dict:
    check_file_exists()
    with open(path,'r') as f:
        d = json.load(f)
        return d

def update_data(path,data) -> dict:
    if data:
        check_file_exists()
        with open(path,'w') as f:
            json.dump(data,f,indent=10)
 
check_file_exists() #<- check DB exist 

users_data : dict = retrive_data(PATHS[0])
data : dict = retrive_data(PATHS[1])
temp_journal : dict = {
        'completed' : [],
        'not_completed' : [],
        'mood' : 0,
        'productivity' : 0,
        'stress_level' : 0,
        'social_interaction' : 0,
        'energy_level': 0,
        'lessons' : '',
        'thankful' : [],
        'sucks' : ''    
        }


# data : dict = {
#     '3cc4505f-3678-414c-b544-e26555728b9c':{
#         1726056000 : {
#         'completed' : ['Go for a walk','Call vasu'],
#         'not_completed' : ['Complete Abyss 12'],
#         'mood' : 4,
#         'productivity' : 5,
#         'stress_level' : 1,
#         'social_interaction' : 0,
#         'energy_level': 4,
#         'lessons' : 'do or die',
#         'thankful' : ['Still alive','Having lovely parents'],
#         'sucks' : 'waking up at 5 am.'    
#         },
#         1726228800 : {
#         'completed' : ['Completed 10000 steps'],
#         'not_completed' : ['Call tuttu'],
#         'mood' : 2,
#         'productivity' : 2,
#         'stress_level' : 4,
#         'social_interaction' : 1,
#         'energy_level': 1,
#         'lessons' : 'do or die',
#         'thankful' : ['Still alive','Having lovely parents'],
#         'sucks' : 'Same as usual, waking up at 5 am.'    
#         },
#         1726358400 : {
#         'completed' : ['Go to temple'],
#         'not_completed' : ['make Onam Pookalam'],
#         'mood' : 4,
#         'productivity' : 5,
#         'stress_level' : 0,
#         'social_interaction' : 5,
#         'energy_level': 4,
#         'lessons' : 'do or die',
#         'thankful' : ['Still alive','Having lovely parents'],
#         'sucks' : 'Same Same, waking up at 5 am.'
#         }
        
#     }
#                 }

# users_data : dict = {
#     '123' : {
#         'email' : '123@gmail.com',
#         'dob' : 976579200000,
#         'id': '3cc4505f-3678-414c-b544-e26555728b9c',
#         'password': '$2b$12$buI43Y8ggvWzgTyqlLoBxupe/ojPEEKbV/mAofu7pCs/JGQWqn.9G'
#     }
# }

class JournalData(BaseModel):
    completed: list
    not_completed: list
    mood: int
    productivity: int
    stress_level: int
    social_interaction: int
    energy_level: int
    lessons: str
    thankful: list
    sucks: str

class RegisterData(BaseModel):
    username: str
    email: str
    dob: int
    password: str

def idgen():
    unique_id = uuid.uuid4()
    return unique_id

@app.get("/")
async def read_root():
    return {
        'Framework': 'FastAPI',
        'version':'0.111.0',
        'author':'JustEmkay'
            }
    
@app.get("/admin/{password}")
async def show_everything(password : str):
    if password == '123':
        return {'users_data' : users_data,
            'journals' : data
            }
    return{
        'data' : None
    }

@app.get("/connection")
async def connection():
    return True

@app.post("/verify/user/{userinput}")
async def verify_user(userinput: str):
    users_data = retrive_data(PATHS[0])
    ud = users_data.keys()
    emails = [users_data[i]['email'] for i in ud]
    if userinput in ud or userinput in emails:
        return False
    return True

@app.post("/verify/username/{uname}")
async def verify_username(uname: str):
    users_data = retrive_data(PATHS[0])
    if uname in users_data:
        return True
    return False

@app.post("/validate/{user_input}/{password}")
async def validate(user_input : str , password : str):
    users_data = retrive_data(PATHS[0])
    ud : list = list (users_data.keys())
    emails : list = [users_data[i]['email'] for i in ud]
    
    if user_input in ud:
        slct_username : str = user_input 
    else:
        if user_input in emails:
            e_indx : int = emails.index(user_input)
            slct_username : str = ud[e_indx]  
        else:
            return {
                'auth':False,
                'user_id': None
                }
    
    user_hash = password.encode('utf-8')
    user_og_hash = users_data[slct_username]['password'].encode()
    result : bool = bcrypt.checkpw(user_hash,user_og_hash)
    if result:
        print(f'id:{users_data[slct_username]["id"]}')
        return {
            'auth': True ,
            'user_id':f'{users_data[slct_username]["id"]}'
            }
    else:
        return {
            'auth':False,
            'user_id': None
            }

@app.post("/register/{tstamp}")
async def validate(tstamp : str ,register_data : RegisterData):
    try:
        users_data = retrive_data(PATHS[0])
        new_id : str = str(idgen() ) 
        users_data.update({
            register_data.username : {
                'id' : new_id,
                'email': register_data.email,
                'dob' : register_data.dob,
                'password' : register_data.password
            }
        })
        
        update_data(PATHS[0],users_data) #<-- update to JSON file
        users_data = retrive_data(PATHS[0])
        
        data = retrive_data(PATHS[1])
        data.update({
            new_id : {
                tstamp : temp_journal
            }
        })
        
        update_data(PATHS[1],data) #<-- update to JSON file
        data = retrive_data(PATHS[1])
        
        return {'status':True}
    
    except Exception as e:
        return {'status':False , 'error': e}
         
 
def create_journal(uid,tstamp) -> None:
    try:
        data = retrive_data(PATHS[1])    
        data[uid].update({str(tstamp) : temp_journal})
        update_data(PATHS[1],data) #<-- update to JSON file
        
    except Exception as e:
        print(f'Create_journal Error:{e}')


@app.post("/journal/{uid}/{tstamp}")
async def update_journal(uid : str,tstamp : str, journal_data: JournalData):
    try:
        data = retrive_data(PATHS[1])
        print("\nbefore data: ",data)
        
        
        data[uid].update({
            tstamp:{
                    "completed": journal_data.completed,
                    "not_completed": journal_data.not_completed,
                    "mood": journal_data.mood,
                    "productivity": journal_data.productivity,
                    "stress_level": journal_data.stress_level,
                    "social_interaction": journal_data.social_interaction,
                    "energy_level": journal_data.energy_level,
                    "lessons": journal_data.lessons,
                    "thankful": journal_data.thankful,
                    "sucks": journal_data.sucks
                    }
                })
         
        update_data(PATHS[1],data) #<-- update to JSON file
        data = retrive_data(PATHS[1])
        
        print("\nafter data: ",data)
        
        journal : dict = data[uid][tstamp]
        status : bool = True
        
        return {'status':status,'data':journal}
    except Exception as e:
        print(f"Error : {e}")
        status : bool = False
        return {'status':status,'data':journal}
    
@app.get("/records/{uid}")
async def get_all_journals(uid:str):
    try:
        data = retrive_data(PATHS[1])
        record_list : list = []
        # if data[uid]:
        print('journal record in data:',data[uid])
        record_list = [i for i in data[uid]]
        print("records:",record_list)
        return {
            'status' : True,
            'data' : record_list,
            'error' : f'Accessed full record list of user'
        }    

    except Exception as e:
        print("Error :",e)
        return {
        'status' : False,
        'data' : [],
        'error' : f'Error Fetching'
    }
    
    
    
@app.get("/journal/{uid}/{tstamp}")
async def get_journal(uid : str,tstamp : str):
    data = retrive_data(PATHS[1])
    
    if uid in data:
        if tstamp in data[uid]:
            return data[uid][tstamp]
        
    create_journal(uid,tstamp)
    data = retrive_data(PATHS[1])
    return data[uid][tstamp]
    
    
    
@app.get("/summerize/{uid}/{slctd_stamp}")
async def get_summary(uid: str, slctd_stamp: str):
    try:
        data = await get_journal(uid, slctd_stamp)
        result = await summer(data) 
        return result
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error summarizing journal: {str(e)}")

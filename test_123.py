import json
companies = {
    
        'companies_name' : [
                            "한국산업",
                            "건한",
                            "나산팀버",
                            "대한테이프",
                            "단가표",
                            "두산종합목재",
                            "삼원목재",
                            "에스디팀버",
                            "온보드",
                            "우진프레임",
                            "원스탑우드",
                            "진양",
                            "케이디우드",
                            "크나우프",
                            "태진목재",
                            "사업자",
                            "기타",
                            "경비_주유소",
                            "경비_경동화물",
                            "경비_대신화물"
            
        ]
}

class JsonReader():
    @staticmethod
    def read(json_file_path):
        with open(json_file_path, 'r', encoding='utf-8') as json_file :
            return json.load(json_file)
    @staticmethod
    def write(json_file_path, data):
        with open(json_file_path, 'w', encoding='utf-8') as json_file:
            json.dump(data, json_file, ensure_ascii=False ,indent=4)
            

    @staticmethod
    def is_data(json_file_path, key, data):
        temp_data = JsonReader.read(json_file_path)
        if key in temp_data :
            if  data in temp_data[key] :
                return temp_data
        return False
            
        
    @staticmethod
    def is_key(json_file_path, key):
        temp_data = JsonReader.read(json_file_path)
        if key in temp_data:
            return temp_data
        else :
            return False  
    
    @staticmethod
    def move(json_file_path , from_key, to_key, move_data):
        temp_data = JsonReader.read(json_file_path)
        if from_key in temp_data and move_data in temp_data[from_key] :
            # print(f'there is {move_data}')
            temp_data[to_key].append(move_data)
            temp_data[from_key].remove(move_data)
            JsonReader.write(json_file_path,temp_data)

    @staticmethod
    def add(json_file_path , key, data):
        temp_data = JsonReader.read(json_file_path)
        try :
            if not data in temp_data[key] :
                temp_data[key].append(data)
                JsonReader.write(json_file_path,temp_data)
            else :
                print(f"{data} is already Existed")
        except : 
            pass
            
            
            

# JsonReader.add('./companies_name.json', 'companies_name' , '건한123')
JsonReader.move('./companies_name.json','companies_name','bookmarked_companies_name','경비_대신화물')

# data = JsonReader.read('./companies_name.json')

# del data['test']

# print(JsonReader.write('./companies_name.json' , data))



# if 'bookmarked_companies_name' in test:
#     print("AAAAAAAAAAAAAAAAAAAA")


# t = json.loads(json_companies_name)

# print(t)
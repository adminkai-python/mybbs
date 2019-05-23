from bigweb.utils import mongo_connect




collection = mongo_connect("mytest","user")


collection.insert_one({"email":"1762378@163.com", "confirmed":True, "post":"i ma  dsc dfnjvfdnij fd jifn idfjn jdn "})
user = collection.find_one({"name":"wallace"})
print(user)





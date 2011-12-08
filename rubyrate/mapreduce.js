var map = function() {
    var msg_total = this.messages.length;
    var key = {subject_id: this.subject_id, 
               content: this.subject_content,};
    emit( key, {msg_total: msg_total});
}
var reduce = function(key, values) {
    var total = 0;
    values.forEach(function(doc) {
        total += doc.msg_total;
    });
    return {msg_total: total};
};
var query = {'shared_by':  ObjectId("4ede15f6c7d10e39c1000000") }
var options = {
    "mapreduce" : "chats", 
    "map" : map, 
    "reduce" : reduce, 
    "query": query, 
    "out" : "tags"
};
result = db.runCommand(options)



from pymongo import Connection
import datetime

connection = Connection()
db = connection.rubyrate

db.chats.update({}, {'$set': {'date_modified': datetime.datetime.utcnow()}})



db.chats.find( { 'shared_by' : { $size: 2 } }, {'shared_by': 1} );
cursor = db.chats.find( { 'shared_by' : { '$size': 1 } } ) 
for chat in cursor:
    wish_id = chat['subject_id']  
    wish = db.wishes.find_one({'_id': wish_id } )
    user_id = wish['user_id'] 
    db.chats.update({'_id':chat['_id'] }, {'$push': {'shared_by': user_id}})


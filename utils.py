import sqlite3,hashlib

#----------------------------------Writing--------------------------------

def writePost(title, txt, idu):
    conn = sqlite3.connect('data.db')
    cur = conn.cursor()
    q = "SELECT MAX(pid) FROM posts"
    idp = cur.execute(q).fetchone()[0]
    if idp == None:
        idp = 0
    print idp+1
    q = "INSERT INTO posts(title,content,uid,pid) VALUES(?,?,?,?)"
    cur.execute(q,(title,txt,idu,idp+1))
    conn.commit()
    return idp + 1

def writeComment(txt, idu, idp):
    conn = sqlite3.connect('data.db')
    cur = conn.cursor()
    q = "SELECT MAX(cid) FROM comments"
    idc = cur.execute(q).fetchone()[0]
    if idc == None:
        idc = 0
    print idc+1
    q = "INSERT INTO comments(content,cid,pid,uid) VALUES(?,?,?,?)"
    cur.execute(q,(txt,idc+1,idp,idu))
    conn.commit()

#----------------------------------Deleting-------------------------------
def deleteComment(idc):
    conn = sqlite3.connect('data.db')
    cur = conn.cursor()
    q = "DELETE FROM comments where comment.cid = %d"
    cur.execute(q%idc)
    q = "UPDATE comments SET comment.cid = comment.cid - 1 WHERE comments.cid > %d"
    cur.execute(q%idc)    
    conn.commit()

#----------------------------------Getting--------------------------------

def getCommentsOnPost(idp):
    conn = sqlite3.connect('data.db')
    cur = conn.cursor()
    q = "SELECT * FROM comments WHERE comments.pid = %d"
    result = cur.execute(q%idp)
    comments = []
    for r in result:
        comments.append(r)
    conn.commit()
    return comments

def getUserPosts(idu):
    conn = sqlite3.connect('data.db')
    cur = conn.cursor()
    q = "SELECT * FROM posts WHERE posts.uid = %d"
    result = cur.execute(q%idu)
    posts = []
    for r in result:
        posts.append(r)
    conn.commit()
    return posts

def getPost(idp):
    conn = sqlite3.connect('data.db')
    cur = conn.cursor()
    q = "SELECT * FROM posts WHERE posts.pid = %d"
    result = cur.execute(q%idp).fetchone()
    return result

def getAllPosts():
    conn = sqlite3.connect('data.db')
    cur = conn.cursor()
    q = "SELECT posts.content,posts.pid,posts.uid,users.name,posts.title FROM posts, users WHERE users.id = posts.uid ORDER BY posts.pid DESC"
    cur.execute(q)
    all_rows = cur.fetchall()
    print all_rows
    conn.commit()
    return all_rows

def getAllUsers():
    conn = sqlite3.connect('data.db')
    cur = conn.cursor()
    q = "SELECT users.name FROM users"
    cur.execute(q)
    all_rows = cur.fetchall()
    print all_rows
    conn.commit()
    return all_rows

#----------------------------------Log In---------------------------------
    
def encrypt(word):
    hashp = hashlib.md5()
    hashp.update(word)
    return hashp.hexdigest()

def authenticate(username,password):
    conn = sqlite3.connect('data.db')
    cur = conn.cursor()
    q = 'SELECT users.password FROM users WHERE users.name = "%s"'
    result = cur.execute(q%username)
    for r in result:
        if(encrypt(password) == r[0]):
            return True
    return False

def getUserId(name):
    conn = sqlite3.connect('data.db')
    cur = conn.cursor()
    q = 'SELECT users.id FROM users WHERE users.name = "%s"'
    result = cur.execute(q%name).fetchone()
    return result[0]

def getUserName(uid):
    conn = sqlite3.connect('data.db')
    cur = conn.cursor()
    q = 'SELECT users.name FROM users WHERE users.id = %d'
    result = cur.execute(q%name).fetchone()
    return result[0]

def addUser(username,password,pic):
    conn = sqlite3.connect('data.db')
    cur = conn.cursor()
    q = 'SELECT users.name FROM users WHERE users.name = ?'
    result = cur.execute(q,(username,)).fetchone()
    if result == None:
        q = 'SELECT max(users.id) FROM users'
        uid = cur.execute(q).fetchone()[0]
        if uid==None:
            uid=0
        q = 'INSERT INTO users VALUES (?, ?, ?, ?)'
        cur.execute(q, (username, encrypt(password), uid+1, pic))
        print str(uid+1)+","+username
        conn.commit()
        return True
    return False

#addUser("what is this","efdsf")
#addUser("snaddy project","eeefef")
#addUser("more users","gggggg")
#addUser("ok this is the last","dfsdf")

#writePost("im sandy",2)
#writePost("call me white fang",3)
#writePost("im also white bread",4)
#writePost("im the leader fear me",1)
#writePost("i joined track to run away from my problems",3)
#writePost("kms",2)
#writePost("sandy candy pt 4","i may be candy but im not sweet ;)",1)

#writeComment("lol i hate u",1,2)
#writeComment("who do u think u r",3,3)
#writeComment("gr8 work snad",1,4)
#writeComment("maybe your creativity should join the track team",3,6)
    
#print getUserPosts(1)
#print getUserPosts(2)
#print getUserPosts(3)
#print getUserPosts(4)

#print getCommentsOnPost(4)
#print getCommentsOnPost(6)
#print getCommentsOnPost(7)


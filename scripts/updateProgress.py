import sys
if sys.version_info < (3,0):
    from urllib import urlopen
    fileHeader = "/user/schafer/web/outreach/dojo/"
else:
    from urllib.request import urlopen
    fileHeader = "../"

exclusionList = ["CVCoderDojo","jbschafer","uniscratch"]
approvalList = ["CVCoderDojo","jbschafer","uniscratch","crogersaea267"]
website = "http://www.cs.uni.edu/~schafer/outreach/dojo/"
#columnsVisible = 3
maxShown = 4
newCount = 10


#mode 0=all from files  (For HTML development purposes)
#mode 1=update gallery list only  (Only needed if new materials have been added to curriculum)
#                                 This mode requires some additional manual intervention of
#                                 gallery list file after the fact
#mode 2=update user submission lists only  (Most common mode on website)
#mode 3=update both gallery and user submission lists
def generatePages(mode=0):
    #Get Gallery List
    if mode==1 or mode==3:
        print("Updating Gallery List")
        parseAllGalleries()
        print("Do not forget to manually order and add instruction links")
        
    print("Reading in Gallery List")
    fin = open(fileHeader+"scripts/galleryIndex.txt","r")
    galleries = []
    lines = []
    for line in fin:
        if line.find("|")>-1:
            toks = line.split("|")
            if toks[1].find("Debug")==-1:
                galleries.append(int(toks[0]))
                lines.append(line)
    fin.close()
    print(str(len(galleries))+" galleries found")

    #If necessary, scrape each gallery website again for user activity
    if mode==2 or mode==3:
        print("Updating submission lists for galleries ")
        for gid in galleries:
            galleryIDScrape(gid)


    #Generate results tables
            
    #createHTMLTables(galleries,lines)
    createWIKITables(galleries,lines)


def createHTMLTables(galleries,lines):
    from datetime import datetime
    from datetime import timedelta
    current=str(datetime.now())
    tdelta = timedelta(days=newCount)
    
    #Read through the gallery files to make a list of users present
    allUsers = {}
    users = []
    for gid in galleries:
        fin = open(fileHeader+"scripts/"+str(gid)+".txt","r")
        for line in fin:
            toks = line.split("|")
            uid = toks[0]
            pid = toks[1]
            discovered = toks[2]
            comments = toks[3]
            if not uid in exclusionList:
                #pid=pid[:-1]
                if not uid in allUsers:
                    allUsers[uid]=[]
                    users.append(uid)
                allUsers[uid].append((gid,pid,discovered,comments))
    users = sorted(users, key=str.lower)

    #determine how many levels/pages to create
    levels = []
    for item in lines:
        gid,gname,ginst=item.split("|")
        where = ginst.find(":")
        level = ginst[:where]
        if not level in levels:
            levels.append(level)
    levels = sorted(levels,key=str.lower)


    for lev in levels:
        #build single webpage
        web = open(fileHeader+"scripts/projects_"+str(lev)+".html","w")
        web.write("""<!doctype html>
    <html>
    <head>
    <meta charset="utf-8">
    <title>Cedar Valley CoderDojo</title>
    </head>

    <body>
    <h1>CV CoderDojo Ninja Projects Level """)
        web.write(str(lev[3:]))
        web.write("</h1>\n")
        web.write("""<p>Click on a link below to view projects from another level.
                  <ul>\n""")

        for others in levels:
            web.write('<li><a href="projects_'+str(others)+'.html">Level '+others[3:]+'</a></li>\n')
    
            
        web.write("""</ul>
    <p>Clicking on an icon in the table will take you to that Ninja's project.
    <table border="2">
      <tbody>
        <tr>
              <th scope="col">&nbsp;</th>\n""")
        for item in lines:
            gid,gname,ginst=item.split("|")
            if ginst.find(lev)>-1:
                where = gname.find(" - ")
                web.write('      <th scope="col">')
                web.write(gname[where+3:]+'<p>\n')
                web.write('<a href="'+website+'doku.php?id='+ginst+'/">')
                web.write("Instructions")
                web.write('</a><p>\n')
                web.write('<a href="http://scratch.mit.edu/studios/'+gid+'/">')
                web.write("Project Gallery")
                web.write('</a>\n')

        web.write("</tr>\n")

        for uid in users:
            web.write("      <tr>\n")
            web.write('      <th align="left" scope="row">')
            web.write('<a href="http://scratch.mit.edu/users/'+uid+'/">'+uid)
            web.write('</a></th>\n')
            for item in lines:
                gid,gname,ginst=item.split("|")
                #print(gid)
                if ginst.find(lev)>-1:
                    count=0
                    web.write("      <td>")
                    for tup in allUsers[uid]:
                        if gid==str(tup[0]):
                            if count<maxShown:
                                web.write('<a href="http://scratch.mit.edu/projects/'+str(tup[1])+'/">')
                                if tup[3]=="COMMENTS\n":
                                    exist="app"
                                else:
                                    exist="unapp"
 
                                cur=datetime.strptime(current[:current.find(".")], '%Y-%m-%d %H:%M:%S')
                                older=datetime.strptime(tup[2][:tup[2].find(".")], '%Y-%m-%d %H:%M:%S')

                                diff = cur-older

                                if (diff>tdelta):
                                    when="exist"
                                else:
                                    when="new"
                                
                                web.write('<img src="'+when+"_"+exist+'.png">')    
                                web.write('</a>')
                            elif count==maxShown:
                                web.write(" plus more!")
                            count+=1
                    if count==0:
                        web.write('<img src="blank.png">')
                    web.write('&nbsp;</td>\n')
            web.write("    </tr>")

        web.write("""  </tbody>
    </table>
    """)

        web.write("<p>This table last updated:  ")
        current=str(datetime.now())
        bp = current.find(".")
        web.write(current[:bp])
        web.write('<a href="scratchScrape.cgi">.</a>')
        web.write("""</p>
    <p>&nbsp;</p>
    <p>&nbsp;</p>
    </body>
    </html>""")
        web.close()
    




def createWIKITables(galleries,lines):
    from datetime import datetime
    from datetime import timedelta
    current=str(datetime.now())
    tdelta = timedelta(days=newCount)
    
    #Read through the gallery files to make a list of users present
    allUsers = {}
    users = []
    for gid in galleries:
        fin = open(fileHeader+"scripts/"+str(gid)+".txt","r")
        for line in fin:
            toks = line.split("|")
            uid = toks[0]
            pid = toks[1]
            discovered = toks[2]
            comments = toks[3]
            if not uid in exclusionList:
                #pid=pid[:-1]
                if not uid in allUsers:
                    allUsers[uid]=[]
                    users.append(uid)
                allUsers[uid].append((gid,pid,discovered,comments))
    users = sorted(users, key=str.lower)

    #determine how many levels/pages to create
    levels = []
    for item in lines:
        gid,gname,ginst=item.split("|")
        where = ginst.find(":")
        level = ginst[:where]
        if not level in levels:
            levels.append(level)
    levels = sorted(levels,key=str.lower)


    for lev in levels:
        #build single webpage
        web = open(fileHeader+"/data/pages/progress/projects_"+str(lev)+".txt","w")
        web.write("""====== CV CoderDojo Ninja Projects Level """)
        web.write(str(lev[3:]))
        web.write(" ======\n")
        web.write("""Click on a link below to view projects from another level.\n""")

        for others in levels:
            web.write('    *  [[projects_'+str(others)+'|Level '+others[3:]+']]\n')
    
            
        web.write("""\n\nClicking on an icon in the table will take you to that Ninja's project.
    \n\n|  ^""")
        for item in lines:
            gid,gname,ginst=item.split("|")
            if ginst.find(lev)>-1:
                where = gname.find(" - ")
                web.write(gname[where+3:])  #Assignment Name
                web.write('  [['+ginst[:-1]+'|Instructions]]')  #Instruction Link
                web.write('  [[http://scratch.mit.edu/studios/'+gid+'/|ProjectGallery]]') #GalleryLink
                web.write(' ^')
        web.write("\n")

        for uid in users:
            web.write('^  [[http://scratch.mit.edu/users/'+uid+'/|'+uid+']]')
            for item in lines:
                gid,gname,ginst=item.split("|")
                if ginst.find(lev)>-1:
                    count=0
                    web.write(" | ")
                    for tup in allUsers[uid]:
                        if gid==str(tup[0]):
                            if count<maxShown:
                                if tup[3]=="COMMENTS\n":
                                    exist="app"
                                else:
                                    exist="unapp"

                                cur=datetime.strptime(current[:current.find(".")], '%Y-%m-%d %H:%M:%S')
                                older=datetime.strptime(tup[2][:tup[2].find(".")], '%Y-%m-%d %H:%M:%S')

                                diff = cur-older

                                if (diff>tdelta):
                                    when="exist"
                                else:
                                    when="new"

                                web.write('[[http://scratch.mit.edu/projects/'+str(tup[1])+'/|')
                                web.write('{{..:'+when+"_"+exist+'.png|}}]] ')    
                            elif count==maxShown:
                                web.write(" plus more!")
                            count+=1
                    #if count==0:
                        #web.write('{{..:blank.png|}}')    
            web.write(" | \n")


        web.write("This table last updated:  ")
        current=str(datetime.now())
        bp = current.find(".")
        web.write(current[:bp])
        web.close()




#This gets run in mode 2 or 3.  It is used to visit the Scratch website for the given studio
#And it rebuilds the local text file representing what projects are in the studio,
#if they are "new" or not, and if they have been commented on by dojo mentors.
def galleryIDScrape(studio):
    from datetime import datetime
    current=str(datetime.now())
    fname = "scripts/"+str(studio)+".txt"

    #begin by checking contents of existing studio file so that
    #we don't waste time rechecking already checked in projects
    import os.path
    existing=[]
    if os.path.isfile(fileHeader+fname):
        fin = open(fileHeader+fname,"r")
        for rec in fin:
            existing.append(rec)
    
    #Now update this data by checking to see if any of the non-approved projects
    #are now approved
    for index in range(len(existing)):
        rec = existing[index]
        if rec.find("AWAITING")>-1:
            toks = rec.split("|")
            if len(toks)!=4:
                print("OOPS")
            project = toks[1]
            #print(project)
            aResp = urlopen("http://scratch.mit.edu/site-api/comments/project/"+str(project))
            webPg = str(aResp.read())
            for admin in approvalList:
                if webPg.find("users/"+admin)>-1:
                    toks[3]="COMMENTS\n"
                    existing[index]="|".join(toks)
            
            
    #Check the Scratch gallery for new entries
    aResp = urlopen("http://scratch.mit.edu/site-api/projects/in/"+str(studio)+"/1/")
    webPg = str(aResp.read())
    tokens = webPg.split('data-id="')
    for v in tokens[1:]:
        end = v.find('"')
        pid = v[:end]
        
        v2 = v.split("/users/")
        end = v2[1].find("/")
        uid = v2[1][:end]

        found=False
        for rec in existing:
            if rec.find(pid)>-1 and rec.find(uid)>-1:
                found=True
        if not found:
            line = uid+"|"+pid+"|"+str(current)+"|AWAITING\n"
            existing.append(line)

    #now rewrite the whole file                
    fout = open(fileHeader+fname,"w")
    for line in existing:
        fout.write(line)
    fout.close()




def parseAllGalleries():
    #This assumes that the galleryIndex exists and works
    #in "updating" mode.
    fin = open(fileHeader+"scripts/galleryIndex.txt","r")
    existing = []
    lines = []
    for line in fin:
        if line.find("|")>-1:
            toks = line.split("|")
            existing.append(int(toks[0]))
            lines.append(line)
    fin.close()
    print("We already knew about "+str(len(existing))+" galleries.")

    #Now see what is on the website
    aResp = urlopen("http://scratch.mit.edu/site-api/galleries/owned_or_curated_by/CVCoderDojo/")
    webPg = str(aResp.read())
    gals = webPg.split("}}},")
    print(str(len(gals))+" galleries located on scratch website")
    if (len(existing)<len(gals)):
        #This means there are new galleries to add to the list
        print("That means we have to update the list")

        #First, print the old part of the file in current order
        fout = open(fileHeader+"galleryIndex.txt","w")
        for x in lines:
            fout.write(x)

        #Now, find all of the current galleries not already in the file
        newGals = []
        for g in gals:
            colon = g.find(":")
            comma = g.find(",",colon)
            sid = g[colon+2:comma]
            titleTag = g.find('"title": "')
            quote = g.find('"',titleTag+11)
            title = g[titleTag+10:quote]
            if (not (int(sid) in existing)):
                newGals.append((sid,title))
        print("Reality check.  I found "+str(len(newGals))+" new galleries.")
        newGals.sort()
        for g in newGals:
            sid,title=g
            fout.write(sid+"|"+title+"\n")
        fout.close()
    else:
        print("Current File was up to date")


generatePages(2)

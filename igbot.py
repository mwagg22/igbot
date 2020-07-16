from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import random


class InstagramBot:
    followersList=[]
    followingList=[]
    notFollowingMe=[]
    tagLinks=[]
    exploreLinks=[]
    commentsList=['lol','Nice!!!','Awesome Post!','cool']
    likeLimit=300
    unfollowLimit=200
    commentLimit=180
    
    def __init__(self,username,password):
        self.username = username
        self.password = password
        self.bot = webdriver.Firefox()
        
    def login(self):
        bot = self.bot
        bot.get('https://instagram.com/')
        time.sleep(6)
        email = bot.find_element_by_name('username')
        password = bot.find_element_by_name('password')
        email.clear()
        password.clear()
        email.send_keys(self.username)
        password.send_keys(self.password)
        password.send_keys(Keys.RETURN)
        time.sleep(4)

    def GetNames(self):
        bot=self.bot
        height=0
        newHeight=1
        namesList=[]
        scrollElement=bot.find_element_by_xpath("/html/body/div[4]/div/div/div[2]")
        while height!=newHeight:
            time.sleep(2)
            height=newHeight
            bot.execute_script("arguments[0].scrollTo(0,arguments[0].scrollHeight);",scrollElement)
            newHeight=bot.execute_script("return arguments[0].scrollHeight;",scrollElement)
        time.sleep(1)
        lists=bot.find_elements_by_class_name('FPmhX')
        for names in lists:
            try:
                #print(names.get_attribute("title"))
                namesList.append(names.get_attribute("title"))
            except:
                lists=bot.find_elements_by_class_name('FPmhX')
        #print(namesList)
        return namesList
    
    def CheckFollowers(self):
        bot = self.bot
        bot.find_element_by_xpath("//a[contains(@href,'followers')]").click()
        time.sleep(3)
        self.followersList=self.GetNames()
        bot.find_element_by_xpath("/html/body/div[4]/div/div/div[1]/div/div[2]/button").click()
        return 1
         
    def CheckFollowing(self):
        bot = self.bot
        bot.find_element_by_xpath("//a[contains(@href,'following')]").click()
        self.followingList=self.GetNames()
        bot.find_element_by_xpath("/html/body/div[4]/div/div/div[1]/div/div[2]/button").click()
        return 1
        
    def CheckProfile(self):
        bot=self.bot
        bot.get('https://instagram.com/'+self.username)
        time.sleep(4)

    def CheckNotFollowers(self):
        self.CheckFollowers()
        self.CheckFollowing()
        self.GetUnfollowLiist()
                        

    def GetUnfollowLiist(self):
        #print(self.followersList)
        #print(self.followingList)
        for following in self.followingList:
            if following not in self.followersList:
                self.notFollowingMe.append(following)
        print(self.notFollowingMe)

    def UnfollowUnfollowers(self):
        bot=self.bot
        self.OpenFollowing()
        height=0
        newHeight=1
        scrollElement=bot.find_element_by_xpath("/html/body/div[4]/div/div/div[2]")
        while height!=newHeight:
            time.sleep(2)
            height=newHeight
            bot.execute_script("arguments[0].scrollTo(0,arguments[0].scrollHeight);",scrollElement)
            newHeight=bot.execute_script("return arguments[0].scrollHeight;",scrollElement)
        time.sleep(1)
        lists=bot.find_elements_by_class_name('wo9IH')
        names = [elem.find_elements_by_class_name('FPmhX') for elem in lists]
        buttons = [elem.find_elements_by_class_name('sqdOP') for elem in lists]
        for name in names:
            for n in name:
                title=n.get_attribute("title")
                print(title)
                if title in self.notFollowingMe:
                    indx=self.followingList.index(title)
                    btnIndx=buttons[indx]
                    for btnItem in btnIndx:
                        print(btnItem)
                        btnItem.click()
                        bot.find_element_by_xpath("/html/body/div[5]/div/div/div/div[3]/button[1]").click()
                        time.sleep(1)
            
    def GoToExplorePage(self):
        bot=self.bot
        bot.get("https://instagram.com/explore/")
        time.sleep(2)

    def OpenFollowing(self):
        self.CheckProfile()
        time.sleep(2)
        bot = self.bot
        bot.find_element_by_xpath("//a[contains(@href,'following')]").click()

    def GoToTag(self,tagName):
        bot=self.bot
        bot.get("https://instagram.com/explore/tags/"+tagName)
        time.sleep(3)

    def FollowTag(self):
        bot=self.bot
        bot.find_element_by_xpath("/html/body/div[1]/section/main/header/div[2]/div[1]/button").click()

    def FollowUser(self):
        bot=self.bot
        bot.find_element_by_class_name("oW_lN").click()
        time.sleep(1)

    def GetTagLinks(self):
        bot=self.bot
        elements=bot.find_elements_by_class_name('v1Nh3')
        aTag=[elem.find_elements_by_tag_name('a') for elem in elements]
        for a in aTag:
            for name in a:
                self.tagLinks.append(name.get_attribute("href"))

    def GoToPage(self,href):
        bot=self.bot
        bot.get(href)
        time.sleep(2)

    def LikePost(self):
        bot=self.bot
        bot.find_element_by_xpath("/html/body/div[1]/section/main/div/div[1]/article/div[3]/section[1]/span[1]/button").click()
        time.sleep(1)

    def AutoLikeTags(self,tagName):
        self.GoToTag(tagName)
        self.FollowTag()
        self.GetTagLinks()
        for tags in self.tagLinks:
            self.GoToPage(tags)
            self.LikePost()
            time.sleep(1)
        
    def PostComment(self,comment):
        bot=self.bot
        comments=bot.find_element_by_class_name('Ypffh')
        comments.click()
        comments=bot.find_element_by_class_name('Ypffh')
        comments.send_keys(comment)
        comments.send_keys(Keys.RETURN)
        time.sleep(2)
		
    def AutoComment(self):
        bot=self.bot
        comment=random.choice(self.commentsList)
        self.PostComment(comment)
	
    def GetExploreTagLinks(self):
        bot=self.bot
        elements=bot.find_elements_by_class_name('pKKVh')
        aTag=[elem.find_elements_by_tag_name('a') for elem in elements]
        for a in aTag:
            for name in a:
                self.exploreLinks.append(name.get_attribute("href"))
	
    def AutoLikeExplore(self):
        self.GoToExplorePage()
        self.GetExploreTagLinks()
        for tags in self.exploreLinks:
            self.GoToPage(tags)
            self.LikePost()
            time.sleep(1)
			
    def ScrollDown(self):
        bot=self.bot
        bot.execute_script("window.scrollTo(0,document.body.scrollHeight)")
        time.sleep()

    def Idle(self,delta):
        time.sleep(delta)

      
Bot = InstagramBot("username","password")
Bot.login()
Bot.CheckProfile()

# -*- coding: utf-8 -*-


import time
from naoqi import ALProxy
import threading


class Navig():

    def Config_Navig(self):  # Configurates all the initial things to be used in the main app
        self.Robot_IP = "192.168.0.112"
        self.Navigation = ALProxy("ALNavigation", self.Robot_IP, 9559)# 机器人导航模块
        self.Posture = ALProxy("ALRobotPosture", self.Robot_IP, 9559)# 机器人姿态模块
        self.Motion = ALProxy("ALMotion", self.Robot_IP, 9559)# 机器人运动模块
        self.ASR = ALProxy("ALSpeechRecognition", self.Robot_IP, 9559)# 语音识别模块
        self.Memory = ALProxy("ALMemory", self.Robot_IP, 9559)# 记忆模块
        self.Blinking = ALProxy("ALAutonomousBlinking", self.Robot_IP, 9559)# 机器人眨眼
        self.Listening = ALProxy("ALListeningMovement", self.Robot_IP, 9559)# 听
        self.Speak = ALProxy("ALTextToSpeech", self.Robot_IP, 9559)# 说
        self.SpeakMov = ALProxy("ALSpeakingMovement", self.Robot_IP, 9559)# 说话动作
        self.AnimSpeech = ALProxy("ALAnimatedSpeech", self.Robot_IP, 9559)# 机器人说话动画？
        self.Localization = ALProxy("ALLocalization", self.Robot_IP, 9559)# 机器人定位功能模块
        self.TabletService = ALProxy("ALTabletService", self.Robot_IP, 9559)# 控制机器人平板电脑功能

        self.channel = 0
        self.d_Table = 0
        self.l_Table = 0
        self.d_CardChair = 0
        self.l_CardChair = 0
        self.d_Booth = 0
        self.l_Booth = 0
        self.start = "前门"
        self.start2 = ""

        self.order = "您所点的内容是"
        self.order1 = "您所点的内容是"

        # self.a = 2 * self.channel + self.d_Table + self.d_Booth
        self.d_10_9 = 0.0

        self.x = 1.18
        self.y = 0.6
        self.a = 1.4
        self.b = 1.5
        self.r = 1.3

        self.place1 = [0.14076778292655945, -0.1432720273733139, -2.2191553115844727]
        self.place2 = [1.2326278686523438, -1.69862961769104, -0.34953048825263977]
        self.place3 = [0.44239214062690735, -3.1952054500579834, -2.653679847717285]

        self.x_yin = 1.0  # Coordinates of point 1 - In this case, Laboratory
        self.y_yin = 0.0
        self.Theta_yin = 0.0

        self.xE = 4.968353271484375  # Coordinates of point 2 - In this case, Entrance
        self.yE = 0.6844285130500793
        self.ThetaE = -0.07399776577949524

        self.xS = -1.6242592334747314  # Coordinates of point 3 - In this case, Stairs
        self.yS = -0.22312086820602417
        self.ThetaS = -2.4569268226623535

        self.x1 = 0.19208349287509918  # Coordinates of point 1 - In this case, Laboratory
        self.y1 = 0.1759951114654541
        self.Theta1 = 1.6244299411773682

        self.x2 = 27.262617111206055  # Coordinates of point 2 - In this case, Entrance
        self.y2 = 16.265079498291016
        self.Theta2 = 96.7493896484375

        # self.ASR.unsubscribe("Test_ASR") # Activate this function only when an erro occurs. When the speech recognition is activated you need to use this, when it's not, don't use this. By default it's unsubscribed.
        # self.Navigation.stopExploration()

        # self.Navigation.stopLocalization()  # Sets the languange and the words that should be recognized by the robot 设置机器人应识别的语言和单词
        self.ASR.setLanguage("Chinese")# 语音识别转换文本
        self.ASR.pause(True)# True代表暂停语音识别，False为继续语音识别
        self.ASR.removeAllContext()# 删除之前的语音识别文本记录
        #
        self.vocabulary1 = ["一号桌", "二号桌", "三号桌", "四号桌", "五号桌", "六号桌", "七号桌", "八号桌", "九号桌",
                            "十号桌",
                            "停止", "起点", "开始", "结束", "点餐", "薯条", "鸡块", "鱼旦", "一口", "椒盐", "豆腐",
                            "不需要", "芋泥", "波波", "豆乳", "芒果"]# 设置关键词
        self.ASR.pause(True)
        self.ASR.setVocabulary(self.vocabulary1, False)# False启用词语定位，词汇表设置成vocabulary1

        # 暂停语音识别模块
        self.ASR.pause(True)

        self.Motion.setOrthogonalSecurityDistance(0.20)  # Sets the security distance for the sensors
        self.Motion.setTangentialSecurityDistance(0.03)
        self.Motion.setExternalCollisionProtectionEnabled("Arms", False)

        self.Blinking.setEnabled(True)
        self.Listening.setEnabled(True)

        self.SpeakMov.setEnabled(True)
        self.configuration = {"bodyLanguageMode": "contextual"}

        self.Motion.wakeUp()
        # self.path = "/home/nao/.local/share/Explorer/2023-06-05T110525.218Z.explo" #path of the map (previously made) - Paste your path here
        self.path = "/home/nao/.local/share/Explorer/2023-06-08T165545.790Z.explo"  # path of the map (previously made) - Paste your path here
        # print "loading"
        # self.Navigation.loadExploration(self.path)  # loads the map
        # self.Navigation.getMetricalMap()
        # self.Navigation.startLocalization()
        # self.Navigation.relocalizeInMap([0, 0,
        #                                  0])  # Setting the origin, must be known by the user. It's the point where the exploration started when the map was made - origin
        # self.Navigation.navigateToInMap([self.x2, self.y2, self.Theta2]) #Place where the user wants the robot to stay waiting for input
        # self.Navigation.wait(self.Navigation.navigateToInMap([self.xE, self.yE, self.ThetaE]), 1)
        self.Posture.goToPosture("StandInit", 0.5)
        # self.Navigation.stopLocalization()

    def Navigation_Process(self):
        print "Thread2 started"
        self.Posture.goToPosture("StandInit", 0.5)
        # self.Navigation.startLocalization()
        # self.Navigation.getMetricalMap()
        self.AnimSpeech.say("你好！pepper很高兴为你服务，请问前往几号桌?", self.configuration)
        print "First Checkpoint"
        while True:

            if self.Word[1] >= 0.400 and self.Word[0] == '一号桌':
                # Recognition of words and moving to the point after receiving the word input
                # self.Navigation.startLocalization()
                print "Place one Checkpoint 1"
                self.Motion.moveTo(self.r + 0.25 * self.x, 0, 0)
                self.Motion.moveTo(0, 0, 0.5 * 3.14)
                # self.Navigation.wait(Moving_Lab1, 1)

                self.AnimSpeech.say("已到达一号桌，请说点餐来开启服务", self.configuration)
                self.ASR.unsubscribe("Test_ASR")
                self.Posture.goToPosture("StandInit", 0.5)
                self.start = '一号桌'
                print "Place one Checkpoint 2"
                # self.ASR.unsubscribe("Test_ASR")
                time.sleep(2)
                # break

            if self.Word[1] >= 0.400 and self.Word[0] == '二号桌':
                # self.Navigation.startLocalization()
                print "Place one Checkpoint 1"
                self.Motion.moveTo(0, self.r + self.y + 0.5 * self.b, 0)
                self.Motion.moveTo(0.25 * self.x + self.r, 0, 0)
                self.Motion.moveTo(0, 0, 0.5 * 3.14)
                # self.Navigation.wait(Moving_Lab1, 1)

                self.AnimSpeech.say("已到达二号桌，请说点餐来开启服务", self.configuration)
                self.ASR.unsubscribe("Test_ASR")
                self.Posture.goToPosture("StandInit", 0.5)
                self.start = '二号桌'
                print "Place one Checkpoint 2"
                # self.ASR.unsubscribe("Test_ASR")
                time.sleep(2)
                # break

            if self.Word[1] >= 0.400 and self.Word[0] == '三号桌':
                # self.Navigation.startLocalization()
                print "Place one Checkpoint 1"
                self.Motion.moveTo(self.r + 0.75 * self.x, 0, 0)
                # self.Motion.moveTo(0, 0, 0.5 * 3.14)
                # self.Navigation.wait(Moving_Lab1, 1)

                self.AnimSpeech.say("已到达三号桌，请说点餐来开启服务", self.configuration)
                self.ASR.unsubscribe("Test_ASR")
                self.Posture.goToPosture("StandInit", 0.5)
                self.start = '三号桌'

                print "Place one Checkpoint 2"
                # self.ASR.unsubscribe("Test_ASR")
                time.sleep(2)
                # break

            if self.Word[1] >= 0.400 and self.Word[0] == '四号桌':
                # self.Navigation.startLocalization()
                print "Place one Checkpoint 1"
                self.Motion.moveTo(0, self.r + self.y + 0.5 * self.b, 0)
                self.Motion.moveTo(0.75 * self.x + self.r, 0, 0)
                self.Motion.moveTo(0, 0, 0.5 * 3.14)
                # self.Navigation.wait(Moving_Lab1, 1)

                self.AnimSpeech.say("已到达四号桌，请说点餐来开启服务", self.configuration)
                self.ASR.unsubscribe("Test_ASR")
                self.Posture.goToPosture("StandInit", 0.5)
                self.start = '四号桌'

                print "Place one Checkpoint 2"
                # self.ASR.unsubscribe("Test_ASR")
                time.sleep(2)
                # break

            if self.Word[1] >= 0.400 and self.Word[0] == '五号桌':
                # self.Navigation.startLocalization()
                print "Place one Checkpoint 1"
                self.Motion.moveTo(self.r + self.a + 1.25 * self.x, 0, 0)
                self.Motion.moveTo(0, 0, 0.5 * 3.14)
                # self.Navigation.wait(Moving_Lab1, 1)

                self.AnimSpeech.say("已到达五号桌，请说点餐来开启服务", self.configuration)
                self.ASR.unsubscribe("Test_ASR")
                self.Posture.goToPosture("StandInit", 0.5)
                self.start = '五号桌'

                print "Place one Checkpoint 2"
                # self.ASR.unsubscribe("Test_ASR")
                time.sleep(2)
                # break

            if self.Word[1] >= 0.400 and self.Word[0] == '六号桌':
                # self.Navigation.startLocalization()
                print "Place one Checkpoint 1"
                self.Motion.moveTo(0, self.r + self.y + 0.5 * self.b, 0)
                self.Motion.moveTo(1.25 * self.x + self.r + self.a, 0, 0)
                # self.Motion.moveTo(0, 0, 0.5 * 3.14)
                # self.Navigation.wait(Moving_Lab1, 1)

                self.AnimSpeech.say("已到达六号桌，请说点餐来开启服务", self.configuration)
                self.ASR.unsubscribe("Test_ASR")
                self.Posture.goToPosture("StandInit", 0.5)
                self.start = '六号桌'

                print "Place one Checkpoint 2"
                # self.ASR.unsubscribe("Test_ASR")
                time.sleep(2)
                # break

            if self.Word[1] >= 0.400 and self.Word[0] == '七号桌':
                # self.Navigation.startLocalization()
                print "Place one Checkpoint 1"
                self.Motion.moveTo(self.r + self.a + 1.75 * self.x, 0, 0)
                self.Motion.moveTo(0, 0, 0.5 * 3.14)
                # self.Navigation.wait(Moving_Lab1, 1)

                self.AnimSpeech.say("已到达七号桌，请说点餐来开启服务", self.configuration)
                self.ASR.unsubscribe("Test_ASR")
                self.Posture.goToPosture("StandInit", 0.5)
                self.start = '七号桌'

                print "Place one Checkpoint 2"
                # self.ASR.unsubscribe("Test_ASR")
                time.sleep(2)
                # break

            if self.Word[1] >= 0.400 and self.Word[0] == '八号桌':
                # self.Navigation.startLocalization()
                print "Place one Checkpoint 1"
                self.Motion.moveTo(0, self.r + self.y + 0.5 * self.b, 0)
                self.Motion.moveTo(1.75 * self.x + self.r + self.a, 0, 0)
                self.Motion.moveTo(0, 0, 0.5 * 3.14)
                # self.Navigation.wait(Moving_Lab1, 1)

                self.AnimSpeech.say("已到达八号桌，请说点餐来开启服务", self.configuration)
                self.ASR.unsubscribe("Test_ASR")
                self.Posture.goToPosture("StandInit", 0.5)
                self.start = '八号桌'

                print "Place one Checkpoint 2"
                # self.ASR.unsubscribe("Test_ASR")
                time.sleep(2)
                # break

            if self.Word[1] >= 0.400 and self.Word[0] == '九号桌':
                # self.Navigation.startLocalization()
                print "Place one Checkpoint 1"
                self.Motion.moveTo(0, self.r + 2 * self.y + 1.5 * self.b, 0)
                self.Motion.moveTo(1.75 * self.x + self.r + self.a, 0, 0)
                self.Motion.moveTo(0, 0, 0.5 * 3.14)
                # self.Navigation.wait(Moving_Lab1, 1)

                self.AnimSpeech.say("已到达九号桌，请说点餐来开启服务", self.configuration)
                self.ASR.unsubscribe("Test_ASR")
                self.Posture.goToPosture("StandInit", 0.5)
                self.start = '九号桌'

                print "Place one Checkpoint 2"
                # self.ASR.unsubscribe("Test_ASR")
                time.sleep(2)
                # break

            if self.Word[1] >= 0.400 and self.Word[0] == '十号桌':
                # self.Navigation.startLocalization()
                print "Place one Checkpoint 1"
                self.Motion.moveTo(0, self.r + 2 * self.y + 1.5 * self.b, 0)
                self.Motion.moveTo(0.75 * self.x + self.r, 0, 0)
                self.Motion.moveTo(0, 0, 0.5 * 3.14)
                # self.Navigation.wait(Moving_Lab1, 1)

                self.AnimSpeech.say("已到达十号桌，请说点餐来开启服务", self.configuration)
                self.ASR.unsubscribe("Test_ASR")
                self.Posture.goToPosture("StandInit", 0.5)
                self.start = '十号桌'

                print "Place one Checkpoint 2"
                # self.ASR.unsubscribe("Test_ASR")
                time.sleep(2)
                # break

        # self.start2 = self.start

    def order_Process(self):  # Function to stop the robot when he recognizes "stop" and goes back to origin
        print "Thread2 started"
        self.order = self.order1
        self.AnimSpeech.say("欢迎光临，请问您需要吃点什么？", self.configuration)
        self.TabletService.showImage("http://192.168.0.112/apps/tablet-browser/1.jpg")

        while True:
            time.sleep(1)
            self.ASR.subscribe("Test_ASR")
            self.Word = self.Memory.getData("WordRecognized")
            data = self.Word[0].decode("utf-8")
            print("Word: ")
            print(data)
            print self.Word[1]
            data = data.encode("utf-8")

            if self.Word[1] >= 0.400 and data == '薯条':
                print "Pepper recognized"
                self.AnimSpeech.say("好的，请问您还需要点什么？如果不需要，请说不需要。", self.configuration)
                self.ASR.unsubscribe("Test_ASR")
                self.order = self.order + "薯条，"

            if self.Word[1] >= 0.400 and data == '鸡块':
                print "Pepper recognized"
                self.AnimSpeech.say("好的，请问您还需要点什么？如果不需要，请说不需要。", self.configuration)
                self.ASR.unsubscribe("Test_ASR")
                self.order = self.order + "鸡块，"

            if self.Word[1] >= 0.500 and data == '鱼旦':
                print "Pepper recognized"
                self.AnimSpeech.say("好的，请问您还需要点什么？如果不需要，请说不需要。", self.configuration)
                self.ASR.unsubscribe("Test_ASR")
                self.order = self.order + "鱼旦，"

            if self.Word[1] >= 0.400 and data == '一口':
                print "Pepper recognized"
                self.AnimSpeech.say("好的，请问您还需要点什么？如果不需要，请说不需要。", self.configuration)
                self.ASR.unsubscribe("Test_ASR")
                self.order = self.order + "一口西多士，"

            if self.Word[1] >= 0.400 and data == '椒盐':
                print "Pepper recognized"
                self.AnimSpeech.say("好的，请问您还需要点什么？如果不需要，请说不需要。", self.configuration)
                self.ASR.unsubscribe("Test_ASR")
                self.order = self.order + "椒盐玉米，"

            if self.Word[1] >= 0.400 and data == '豆腐':
                print "Pepper recognized"
                self.AnimSpeech.say("好的，请问您还需要点什么？如果不需要，请说不需要。", self.configuration)
                self.ASR.unsubscribe("Test_ASR")
                self.order = self.order + "烧汁豆腐，"

            if self.Word[1] >= 0.500 and data == '不需要':
                break
        self.AnimSpeech.say("请问您需要吃点什么甜品？", self.configuration)
        self.TabletService.showImage("http://192.168.0.112/apps/tablet-browser/2.png")

        while True:
            time.sleep(1)
            self.ASR.subscribe("Test_ASR")
            self.Word = self.Memory.getData("WordRecognized")
            data = self.Word[0].decode("utf-8")
            print("Word: ")
            print(data)
            print self.Word[1]
            data = data.encode("utf-8")

            if self.Word[1] >= 0.400 and data == '芋泥':
                print "Pepper recognized"
                self.AnimSpeech.say("好的，请问您还需要点什么？如果不需要，请说不需要。", self.configuration)
                self.ASR.unsubscribe("Test_ASR")
                self.order = self.order + "芋泥鲜果桂花碗，"

            if self.Word[1] >= 0.400 and data == '波波':
                print "Pepper recognized"
                self.AnimSpeech.say("好的，请问您还需要点什么？如果不需要，请说不需要。", self.configuration)
                self.ASR.unsubscribe("Test_ASR")
                self.order = self.order + "桂花波波奶冻碗，"

            if self.Word[1] >= 0.400 and data == '豆乳':
                print "Pepper recognized"
                self.AnimSpeech.say("好的，请问您还需要点什么？如果不需要，请说不需要。", self.configuration)
                self.ASR.unsubscribe("Test_ASR")
                self.order = self.order + "豆乳丸子捞，"

            if self.Word[1] >= 0.400 and data == '芒果':
                print "Pepper recognized"
                self.AnimSpeech.say("好的，请问您还需要点什么？如果不需要，请说不需要。", self.configuration)
                self.ASR.unsubscribe("Te st_ASR")
                self.order = self.order + "士多啤梨芒果斑斓河粉，"

            if self.Word[1] >= 0.500 and data == '不需要':
                break

        self.AnimSpeech.say(self.order, self.configuration)
        self.AnimSpeech.say("请稍等片刻，我将为您献上美食", self.configuration)

    def Navigation_Process2(self):
        print "Thread4 started"
        self.Posture.goToPosture("StandInit", 0.5)
        # self.Navigation.startLocalization()
        # self.Navigation.getMetricalMap()
        self.AnimSpeech.say("你好！pepper很高兴为你服务，请问前往几号桌?", self.configuration)
        print "First Checkpoint"
        if self.start == "一号桌":

            while True:

                if self.Word[1] >= 0.400 and self.Word[
                    0] == '一号桌':  # Recognitio2n of words and moving to the point after receiving the word input
                    # self.Navigation.startLocalization()
                    print "Place one Checkpoint 1"

                    # self.Navigation.wait(Moving_Lab1, 1)

                    self.AnimSpeech.say("已到达一号桌，请说点餐来开启服务", self.configuration)
                    self.ASR.unsubscribe("Test_ASR")
                    self.Posture.goToPosture("StandInit", 0.5)
                    self.start = self.Word[0]
                    print "Place one Checkpoint 2"
                    # self.ASR.unsubscribe("Test_ASR")
                    time.sleep(2)
                    # break

                if self.Word[1] >= 0.400 and self.Word[0] == '二号桌':
                    # self.Navigation.startLocalization()
                    print "Place one Checkpoint 1"
                    self.Motion.moveTo(-self.r - 0.25 * self.x, 0, 0)
                    self.Motion.moveTo(0, self.y + self.r + 0.5 * self.b, 0)
                    self.Motion.moveTo(self.r + 0.25 * self.x, 0, 0)
                    # self.Motion.moveTo(0.5 * self.channel + 0.5 * self.d_Table, 0, 0)
                    # self.Navigation.wait(Moving_Lab1, 1)

                    self.AnimSpeech.say("已到达二号桌，请说点餐来开启服务", self.configuration)
                    self.ASR.unsubscribe("Test_ASR")
                    self.Posture.goToPosture("StandInit", 0.5)
                    self.start = self.Word[0]
                    print "Place one Checkpoint 2"
                    # self.ASR.unsubscribe("Test_ASR")
                    time.sleep(2)
                    # break

                if self.Word[1] >= 0.400 and self.Word[0] == '三号桌':
                    # self.Navigation.startLocalization()
                    print "Place one Checkpoint 1"
                    # self.Motion.moveTo(0, self.a, 0)
                    self.Motion.moveTo(0.5 * self.x, 0, 0)
                    # self.Navigation.wait(Moving_Lab1, 1)

                    self.AnimSpeech.say("已到达三号桌，请说点餐来开启服务", self.configuration)
                    self.ASR.unsubscribe("Test_ASR")
                    self.Posture.goToPosture("StandInit", 0.5)
                    self.start = self.Word[0]
                    print "Place one Checkpoint 2"
                    # self.ASR.unsubscribe("Test_ASR")
                    time.sleep(2)
                    # break

                if self.Word[1] >= 0.400 and self.Word[0] == '四号桌':
                    # self.Navigation.startLocalization()
                    print "Place one Checkpoint 1"
                    self.Motion.moveTo(-self.r - 0.25 * self.x, 0, 0)
                    self.Motion.moveTo(0, self.y + self.r + 0.5 * self.b, 0)
                    self.Motion.moveTo(self.r + 0.75 * self.x, 0, 0)
                    # self.Navigation.wait(Moving_Lab1, 1)

                    self.AnimSpeech.say("已到达四号桌，请说点餐来开启服务", self.configuration)
                    self.ASR.unsubscribe("Test_ASR")
                    self.Posture.goToPosture("StandInit", 0.5)
                    self.start = self.Word[0]
                    print "Place one Checkpoint 2"
                    # self.ASR.unsubscribe("Test_ASR")
                    time.sleep(2)
                    # break

                if self.Word[1] >= 0.400 and self.Word[0] == '五号桌':
                    # self.Navigation.startLocalization()
                    print "Place one Checkpoint 1"
                    # self.Motion.moveTo(0, self.a, 0)
                    self.Motion.moveTo(self.x + self.a, 0, 0)
                    # self.Motion.moveTo(0, 0, 3.14)
                    # self.Navigation.wait(Moving_Lab1, 1)

                    self.AnimSpeech.say("已到达五号桌，请说点餐来开启服务", self.configuration)
                    self.ASR.unsubscribe("Test_ASR")
                    self.Posture.goToPosture("StandInit", 0.5)
                    self.start = self.Word[0]
                    print "Place one Checkpoint 2"
                    # self.ASR.unsubscribe("Test_ASR")
                    time.sleep(2)
                    # break

                if self.Word[1] >= 0.400 and self.Word[0] == '六号桌':
                    # self.Navigation.startLocalization()
                    print "Place one Checkpoint 1"
                    self.Motion.moveTo(0.75 * self.x + 0.5 * self.a, 0, 0)
                    self.Motion.moveTo(0, self.r + self.y + 0.5 * self.b, 0)
                    self.Motion.moveTo(0.25 * self.x + 0.5 * self.a, 0, 0)

                    # self.Navigation.wait(Moving_Lab1, 1)

                    self.AnimSpeech.say("已到达六号桌，请说点餐来开启服务", self.configuration)
                    self.ASR.unsubscribe("Test_ASR")
                    self.Posture.goToPosture("StandInit", 0.5)
                    self.start = self.Word[0]
                    print "Place one Checkpoint 2"
                    # self.ASR.unsubscribe("Test_ASR")
                    time.sleep(2)
                    # break

                if self.Word[1] >= 0.400 and self.Word[0] == '七号桌':
                    # self.Navigation.startLocalization()
                    print "Place one Checkpoint 1"
                    # self.Motion.moveTo(0, self.a, 0)
                    self.Motion.moveTo(1.5 * self.x + self.a, 0, 0)
                    # self.Navigation.wait(Moving_Lab1, 1)

                    self.AnimSpeech.say("已到达七号桌，请说点餐来开启服务", self.configuration)
                    self.ASR.unsubscribe("Test_ASR")
                    self.Posture.goToPosture("StandInit", 0.5)
                    self.start = self.Word[0]
                    print "Place one Checkpoint 2"
                    # self.ASR.unsubscribe("Test_ASR")
                    time.sleep(2)
                    # break

                if self.Word[1] >= 0.400 and self.Word[0] == '八号桌':
                    # self.Navigation.startLocalization()
                    print "Place one Checkpoint 1"
                    self.Motion.moveTo(0.75 * self.x + 0.5 * self.a, 0, 0)
                    self.Motion.moveTo(0, self.r + self.y + 0.5 * self.b, 0)
                    self.Motion.moveTo(0.75 * self.x + 0.5 * self.a, 0, 0)

                    # self.Navigation.wait(Moving_Lab1, 1)

                    self.AnimSpeech.say("已到达八号桌，请说点餐来开启服务", self.configuration)
                    self.ASR.unsubscribe("Test_ASR")
                    self.Posture.goToPosture("StandInit", 0.5)
                    self.start = self.Word[0]
                    print "Place one Checkpoint 2"
                    # self.ASR.unsubscribe("Test_ASR")
                    time.sleep(2)
                    # break

                if self.Word[1] >= 0.400 and self.Word[0] == '九号桌':
                    # self.Navigation.startLocalization()
                    print "Place one Checkpoint 1"
                    self.Motion.moveTo(0.75 * self.x + 0.5 * self.a, 0, 0)
                    self.Motion.moveTo(0, self.r + 2 * self.y + 1.5 * self.b, 0)
                    self.Motion.moveTo(0.5 * self.a + 0.75 * self.x, 0, 0)
                    # self.Navigation.wait(Moving_Lab1, 1)

                    self.AnimSpeech.say("已到达九号桌，请说点餐来开启服务", self.configuration)
                    self.ASR.unsubscribe("Test_ASR")
                    self.Posture.goToPosture("StandInit", 0.5)
                    self.start = self.Word[0]
                    print "Place one Checkpoint 2"
                    # self.ASR.unsubscribe("Test_ASR")
                    time.sleep(2)
                    # break

                if self.Word[1] >= 0.400 and self.Word[0] == '十号桌':
                    # self.Navigation.startLocalization()
                    print "Place one Checkpoint 1"
                    self.Motion.moveTo(0.75 * self.x + 0.5 * self.a, 0, 0)
                    self.Motion.moveTo(0, self.r + 2 * self.y + 1.5 * self.b, 0)
                    self.Motion.moveTo(-0.5 * self.a - 0.25 * self.x, 0, 0)

                    # self.Navigation.wait(Moving_Lab1, 1)

                    self.AnimSpeech.say("已到达十号桌，请说点餐来开启服务", self.configuration)
                    self.ASR.unsubscribe("Test_ASR")
                    self.Posture.goToPosture("StandInit", 0.5)
                    self.start = self.Word[0]
                    print "Place one Checkpoint 2"
                    # self.ASR.unsubscribe("Test_ASR")
                    time.sleep(2)
                    # break

        elif self.start == "二号桌":
            while True:

                if self.Word[1] >= 0.400 and self.Word[
                    0] == '一号桌':  # Recognitio2n of words and moving to the point after receiving the word input
                    # self.Navigation.startLocalization()
                    print "Place one Checkpoint 1"

                    # self.Navigation.wait(Moving_Lab1, 1)
                    self.Motion.moveTo(-0.25 * self.x - self.r, 0, 0)
                    self.Motion.moveTo(0, -0.5 * self.b - self.y - self.r, 0)
                    self.Motion.moveTo(0.25 * self.x + self.r, 0, 0)

                    self.AnimSpeech.say("已到达一号桌，请说点餐来开启服务", self.configuration)
                    self.ASR.unsubscribe("Test_ASR")
                    self.Posture.goToPosture("StandInit", 0.5)
                    self.start = self.Word[0]
                    print "Place one Checkpoint 2"
                    # self.ASR.unsubscribe("Test_ASR")
                    time.sleep(2)
                    # break

                if self.Word[1] >= 0.400 and self.Word[0] == '二号桌':
                    # self.Navigation.startLocalization()
                    print "Place one Checkpoint 1"
                    # self.Motion.moveTo(0.5 * self.channel + 0.5 * self.d_Table, 0, 0)
                    # self.Navigation.wait(Moving_Lab1, 1)

                    self.AnimSpeech.say("已到达二号桌，请说点餐来开启服务", self.configuration)
                    self.ASR.unsubscribe("Test_ASR")
                    self.Posture.goToPosture("StandInit", 0.5)
                    self.start = self.Word[0]
                    print "Place one Checkpoint 2"
                    # self.ASR.unsubscribe("Test_ASR")
                    time.sleep(2)
                    # break

                if self.Word[1] >= 0.400 and self.Word[0] == '三号桌':
                    # self.Navigation.startLocalization()
                    print "Place one Checkpoint 1"
                    # self.Motion.moveTo(0, self.a, 0)
                    self.Motion.moveTo(-0.25 * self.x - self.r, 0, 0)
                    self.Motion.moveTo(0, -0.5 * self.b - self.y - self.r, 0)
                    self.Motion.moveTo(0.75 * self.x + self.r, 0, 0)

                    # self.Navigation.wait(Moving_Lab1, 1)

                    self.AnimSpeech.say("已到达三号桌，请说点餐来开启服务", self.configuration)
                    self.ASR.unsubscribe("Test_ASR")
                    self.Posture.goToPosture("StandInit", 0.5)
                    self.start = self.Word[0]
                    print "Place one Checkpoint 2"
                    # self.ASR.unsubscribe("Test_ASR")
                    time.sleep(2)
                    # break

                if self.Word[1] >= 0.400 and self.Word[0] == '四号桌':
                    # self.Navigation.startLocalization()
                    print "Place one Checkpoint 1"
                    self.Motion.moveTo(0.5 * self.x, 0, 0)
                    # self.Navigation.wait(Moving_Lab1, 1)

                    self.AnimSpeech.say("已到达四号桌，请说点餐来开启服务", self.configuration)
                    self.ASR.unsubscribe("Test_ASR")
                    self.Posture.goToPosture("StandInit", 0.5)
                    self.start = self.Word[0]
                    print "Place one Checkpoint 2"
                    # self.ASR.unsubscribe("Test_ASR")
                    time.sleep(2)
                    # break

                if self.Word[1] >= 0.400 and self.Word[0] == '五号桌':
                    # self.Navigation.startLocalization()
                    print "Place one Checkpoint 1"
                    # self.Motion.moveTo(0, self.a, 0)
                    self.Motion.moveTo(0.75 * self.x + 0.5 * self.a, 0, 0)
                    self.Motion.moveTo(0, -0.5 * self.b - self.y - self.r, 0)
                    self.Motion.moveTo(self.r + 0.25 * self.x, 0, 0)
                    # self.Navigation.wait(Moving_Lab1, 1)

                    self.AnimSpeech.say("已到达五号桌，请说点餐来开启服务", self.configuration)
                    self.ASR.unsubscribe("Test_ASR")
                    self.Posture.goToPosture("StandInit", 0.5)
                    self.start = self.Word[0]
                    print "Place one Checkpoint 2"
                    # self.ASR.unsubscribe("Test_ASR")
                    time.sleep(2)
                    # break

                if self.Word[1] >= 0.400 and self.Word[0] == '六号桌':
                    # self.Navigation.startLocalization()
                    print "Place one Checkpoint 1"
                    self.Motion.moveTo(self.x + self.a, 0, 0)
                    # self.Navigation.wait(Moving_Lab1, 1)

                    self.AnimSpeech.say("已到达六号桌，请说点餐来开启服务", self.configuration)
                    self.ASR.unsubscribe("Test_ASR")
                    self.Posture.goToPosture("StandInit", 0.5)
                    self.start = self.Word[0]
                    print "Place one Checkpoint 2"
                    # self.ASR.unsubscribe("Test_ASR")
                    time.sleep(2)
                    # break

                if self.Word[1] >= 0.400 and self.Word[0] == '七号桌':
                    # self.Navigation.startLocalization()
                    print "Place one Checkpoint 1"
                    # self.Motion.moveTo(0, self.a, 0)
                    self.Motion.moveTo(0.75 * self.x + 0.5 * self.a, 0, 0)
                    self.Motion.moveTo(0, -0.5 * self.b - self.y - self.r, 0)
                    self.Motion.moveTo(self.r + 0.75 * self.x, 0, 0)

                    # self.Navigation.wait(Moving_Lab1, 1)

                    self.AnimSpeech.say("已到达七号桌，请说点餐来开启服务", self.configuration)
                    self.ASR.unsubscribe("Test_ASR")
                    self.Posture.goToPosture("StandInit", 0.5)
                    self.start = self.Word[0]
                    print "Place one Checkpoint 2"
                    # self.ASR.unsubscribe("Test_ASR")
                    time.sleep(2)
                    # break

                if self.Word[1] >= 0.400 and self.Word[0] == '八号桌':
                    # self.Navigation.startLocalization()
                    print "Place one Checkpoint 1"
                    self.Motion.moveTo(1.5 * self.x + self.a, 0, 0)

                    # self.Navigation.wait(Moving_Lab1, 1)

                    self.AnimSpeech.say("已到达八号桌，请说点餐来开启服务", self.configuration)
                    self.ASR.unsubscribe("Test_ASR")
                    self.Posture.goToPosture("StandInit", 0.5)
                    self.start = self.Word[0]
                    print "Place one Checkpoint 2"
                    # self.ASR.unsubscribe("Test_ASR")
                    time.sleep(2)
                    # break

                if self.Word[1] >= 0.400 and self.Word[0] == '九号桌':
                    # self.Navigation.startLocalization()
                    print "Place one Checkpoint 1"
                    self.Motion.moveTo(0.75 * self.x + 0.5 * self.a, 0, 0)
                    self.Motion.moveTo(0, self.b + self.y, 0)
                    self.Motion.moveTo(0.5 * self.a + 0.75 * self.x, 0, 0)
                    # self.Navigation.wait(Moving_Lab1, 1)

                    self.AnimSpeech.say("已到达九号桌，请说点餐来开启服务", self.configuration)
                    self.ASR.unsubscribe("Test_ASR")
                    self.Posture.goToPosture("StandInit", 0.5)
                    self.start = self.Word[0]
                    print "Place one Checkpoint 2"
                    # self.ASR.unsubscribe("Test_ASR")
                    time.sleep(2)
                    # break

                if self.Word[1] >= 0.400 and self.Word[0] == '十号桌':
                    # self.Navigation.startLocalization()
                    print "Place one Checkpoint 1"
                    self.Motion.moveTo(0.75 * self.x + 0.5 * self.a, 0, 0)
                    self.Motion.moveTo(0, self.b + self.y, 0)
                    self.Motion.moveTo(-0.5 * self.a - 0.25 * self.x, 0, 0)

                    # self.Navigation.wait(Moving_Lab1, 1)

                    self.AnimSpeech.say("已到达十号桌，请说点餐来开启服务", self.configuration)
                    self.ASR.unsubscribe("Test_ASR")
                    self.Posture.goToPosture("StandInit", 0.5)
                    self.start = self.Word[0]
                    print "Place one Checkpoint 2"
                    # self.ASR.unsubscribe("Test_ASR")
                    time.sleep(2)
                    # break

        elif self.start == "三号桌":
            while True:
                if self.Word[1] >= 0.400 and self.Word[
                    0] == '一号桌':  # Recognitio2n of words and moving to the point after receiving the word input
                    # self.Navigation.startLocalization()
                    print "Place one Checkpoint 1"

                    self.Motion.moveTo(-0.5 * self.x, 0, 0)

                    self.AnimSpeech.say("已到达一号桌，请说点餐来开启服务", self.configuration)
                    self.ASR.unsubscribe("Test_ASR")
                    self.Posture.goToPosture("StandInit", 0.5)
                    self.start = self.Word[0]
                    print "Place one Checkpoint 2"
                    # self.ASR.unsubscribe("Test_ASR")
                    time.sleep(2)
                    # break

                if self.Word[1] >= 0.400 and self.Word[0] == '二号桌':
                    # self.Navigation.startLocalization()
                    print "Place one Checkpoint 1"
                    self.Motion.moveTo(-self.r - 0.75 * self.x, 0, 0)
                    self.Motion.moveTo(0, self.y + self.r + 0.5 * self.b, 0)
                    self.Motion.moveTo(self.r + 0.25 * self.x, 0, 0)
                    # self.Motion.moveTo(0.5 * self.channel + 0.5 * self.d_Table, 0, 0)
                    # self.Navigation.wait(Moving_Lab1, 1)

                    self.AnimSpeech.say("已到达二号桌，请说点餐来开启服务", self.configuration)
                    self.ASR.unsubscribe("Test_ASR")
                    self.Posture.goToPosture("StandInit", 0.5)
                    self.start = self.Word[0]
                    print "Place one Checkpoint 2"
                    # self.ASR.unsubscribe("Test_ASR")
                    time.sleep(2)
                    # break

                if self.Word[1] >= 0.400 and self.Word[0] == '三号桌':
                    # self.Navigation.startLocalization()
                    print "Place one Checkpoint 1"
                    # self.Motion.moveTo(0, self.a, 0)
                    self.Motion.moveTo(0, 0, 0)
                    # self.Navigation.wait(Moving_Lab1, 1)

                    self.AnimSpeech.say("已到达三号桌，请说点餐来开启服务", self.configuration)
                    self.ASR.unsubscribe("Test_ASR")
                    self.Posture.goToPosture("StandInit", 0.5)
                    self.start = self.Word[0]
                    print "Place one Checkpoint 2"
                    # self.ASR.unsubscribe("Test_ASR")
                    time.sleep(2)
                    # break

                if self.Word[1] >= 0.400 and self.Word[0] == '四号桌':
                    # self.Navigation.startLocalization()
                    print "Place one Checkpoint 1"
                    # self.Motion.moveTo(self.d_Table, 0, 0)
                    self.Motion.moveTo(-self.r - 0.75 * self.x, 0, 0)
                    self.Motion.moveTo(0, self.y + self.r + 0.5 * self.b, 0)
                    self.Motion.moveTo(self.r + 0.75 * self.x, 0, 0)
                    # self.Navigation.wait(Moving_Lab1, 1)

                    self.AnimSpeech.say("已到达四号桌，请说点餐来开启服务", self.configuration)
                    self.ASR.unsubscribe("Test_ASR")
                    self.Posture.goToPosture("StandInit", 0.5)
                    self.start = self.Word[0]
                    print "Place one Checkpoint 2"
                    # self.ASR.unsubscribe("Test_ASR")
                    time.sleep(2)
                    # break

                if self.Word[1] >= 0.400 and self.Word[0] == '五号桌':
                    # self.Navigation.startLocalization()
                    print "Place one Checkpoint 1"
                    # self.Motion.moveTo(0, self.a, 0)
                    self.Motion.moveTo(self.a + 0.5 * self.x, 0, 0)
                    # self.Motion.moveTo(0, 0, 3.14)
                    # self.Navigation.wait(Moving_Lab1, 1)

                    self.AnimSpeech.say("已到达五号桌，请说点餐来开启服务", self.configuration)
                    self.ASR.unsubscribe("Test_ASR")
                    self.Posture.goToPosture("StandInit", 0.5)
                    self.start = self.Word[0]
                    print "Place one Checkpoint 2"
                    # self.ASR.unsubscribe("Test_ASR")
                    time.sleep(2)
                    # break

                if self.Word[1] >= 0.400 and self.Word[0] == '六号桌':
                    # self.Navigation.startLocalization()
                    print "Place one Checkpoint 1"
                    self.Motion.moveTo(0.25 * self.x + 0.5 * self.a, 0, 0)
                    self.Motion.moveTo(0, self.r + self.y + 0.5 * self.b, 0)
                    self.Motion.moveTo(0.25 * self.x + 0.5 * self.a, 0, 0)
                    # self.Navigation.wait(Moving_Lab1, 1)

                    self.AnimSpeech.say("已到达六号桌，请说点餐来开启服务", self.configuration)
                    self.ASR.unsubscribe("Test_ASR")
                    self.Posture.goToPosture("StandInit", 0.5)
                    self.start = self.Word[0]
                    print "Place one Checkpoint 2"
                    # self.ASR.unsubscribe("Test_ASR")
                    time.sleep(2)
                    # break

                if self.Word[1] >= 0.400 and self.Word[0] == '七号桌':
                    # self.Navigation.startLocalization()
                    print "Place one Checkpoint 1"
                    # self.Motion.moveTo(0, self.a, 0)
                    self.Motion.moveTo(self.a + 0.75 * self.x, 0, 0)
                    # self.Navigation.wait(Moving_Lab1, 1)

                    self.AnimSpeech.say("已到达七号桌，请说点餐来开启服务", self.configuration)
                    self.ASR.unsubscribe("Test_ASR")
                    self.Posture.goToPosture("StandInit", 0.5)
                    self.start = self.Word[0]
                    print "Place one Checkpoint 2"
                    # self.ASR.unsubscribe("Test_ASR")
                    time.sleep(2)
                    # break

                if self.Word[1] >= 0.400 and self.Word[0] == '八号桌':
                    # self.Navigation.startLocalization()
                    print "Place one Checkpoint 1"
                    self.Motion.moveTo(0.25 * self.x + 0.5 * self.a, 0, 0)
                    self.Motion.moveTo(0, self.r + self.y + 0.5 * self.b, 0)
                    self.Motion.moveTo(0.75 * self.x + 0.5 * self.a, 0, 0)

                    # self.Navigation.wait(Moving_Lab1, 1)

                    self.AnimSpeech.say("已到达八号桌，请说点餐来开启服务", self.configuration)
                    self.ASR.unsubscribe("Test_ASR")
                    self.Posture.goToPosture("StandInit", 0.5)
                    self.start = self.Word[0]
                    print "Place one Checkpoint 2"
                    # self.ASR.unsubscribe("Test_ASR")
                    time.sleep(2)
                    # break

                if self.Word[1] >= 0.400 and self.Word[0] == '九号桌':
                    # self.Navigation.startLocalization()
                    print "Place one Checkpoint 1"
                    self.Motion.moveTo(0.25 * self.x + 0.5 * self.a, 0, 0)
                    self.Motion.moveTo(0, self.r + 2 * self.y + 1.5 * self.b, 0)
                    self.Motion.moveTo(0.5 * self.a + 0.75 * self.x, 0, 0)
                    # self.Navigation.wait(Moving_Lab1, 1)

                    self.AnimSpeech.say("已到达九号桌，请说点餐来开启服务", self.configuration)
                    self.ASR.unsubscribe("Test_ASR")
                    self.Posture.goToPosture("StandInit", 0.5)
                    self.start = self.Word[0]
                    print "Place one Checkpoint 2"
                    # self.ASR.unsubscribe("Test_ASR")
                    time.sleep(2)
                    # break

                if self.Word[1] >= 0.400 and self.Word[0] == '十号桌':
                    # self.Navigation.startLocalization()
                    print "Place one Checkpoint 1"
                    self.Motion.moveTo(0.25 * self.x + 0.5 * self.a, 0, 0)
                    self.Motion.moveTo(0, self.r + 2 * self.y + 1.5 * self.b, 0)
                    self.Motion.moveTo(-0.5 * self.a - 0.25 * self.x, 0, 0)

                    # self.Navigation.wait(Moving_Lab1, 1)

                    self.AnimSpeech.say("已到达十号桌，请说点餐来开启服务", self.configuration)
                    self.ASR.unsubscribe("Test_ASR")
                    self.Posture.goToPosture("StandInit", 0.5)
                    self.start = self.Word[0]
                    print "Place one Checkpoint 2"
                    # self.ASR.unsubscribe("Test_ASR")
                    time.sleep(2)
                    # break


        elif self.start == "四号桌":
            while True:
                if self.Word[1] >= 0.400 and self.Word[
                    0] == '一号桌':  # Recognitio2n of words and moving to the point after receiving the word input
                    # self.Navigation.startLocalization()
                    print "Place one Checkpoint 1"

                    self.Motion.moveTo(-0.75 * self.x - self.r, 0, 0)
                    self.Motion.moveTo(0, -0.5 * self.b - self.y - self.r, 0)
                    self.Motion.moveTo(0.25 * self.x + self.r, 0, 0)

                    self.AnimSpeech.say("已到达一号桌，请说点餐来开启服务", self.configuration)
                    self.ASR.unsubscribe("Test_ASR")
                    self.Posture.goToPosture("StandInit", 0.5)
                    self.start = self.Word[0]
                    print "Place one Checkpoint 2"
                    # self.ASR.unsubscribe("Test_ASR")
                    time.sleep(2)
                    # break

                if self.Word[1] >= 0.400 and self.Word[0] == '二号桌':
                    # self.Navigation.startLocalization()
                    print "Place one Checkpoint 1"
                    self.Motion.moveTo(-0.5 * self.x, 0, 0)
                    # self.Motion.moveTo(0.5 * self.channel + 0.5 * self.d_Table, 0, 0)
                    # self.Navigation.wait(Moving_Lab1, 1)

                    self.AnimSpeech.say("已到达二号桌，请说点餐来开启服务", self.configuration)
                    self.ASR.unsubscribe("Test_ASR")
                    self.Posture.goToPosture("StandInit", 0.5)
                    self.start = self.Word[0]
                    print "Place one Checkpoint 2"
                    # self.ASR.unsubscribe("Test_ASR")
                    time.sleep(2)
                    # break

                if self.Word[1] >= 0.400 and self.Word[0] == '三号桌':
                    # self.Navigation.startLocalization()
                    print "Place one Checkpoint 1"
                    # self.Motion.moveTo(0, self.a, 0)
                    self.Motion.moveTo(-0.75 * self.x - self.r, 0, 0)
                    self.Motion.moveTo(0, -0.5 * self.b - self.y - self.r, 0)
                    self.Motion.moveTo(0.75 * self.x + self.r, 0, 0)

                    # self.Navigation.wait(Moving_Lab1, 1)

                    self.AnimSpeech.say("已到达三号桌，请说点餐来开启服务", self.configuration)
                    self.ASR.unsubscribe("Test_ASR")
                    self.Posture.goToPosture("StandInit", 0.5)
                    self.start = self.Word[0]
                    print "Place one Checkpoint 2"
                    # self.ASR.unsubscribe("Test_ASR")
                    time.sleep(2)
                    # break

                if self.Word[1] >= 0.400 and self.Word[0] == '四号桌':
                    # self.Navigation.startLocalization()
                    print "Place one Checkpoint 1"
                    # self.Motion.moveTo(self.d_Table, 0, 0)
                    # self.Navigation.wait(Moving_Lab1, 1)
                    self.Motion.moveTo(0, 0, 0)

                    self.AnimSpeech.say("已到达四号桌，请说点餐来开启服务", self.configuration)
                    self.ASR.unsubscribe("Test_ASR")
                    self.Posture.goToPosture("StandInit", 0.5)
                    self.start = self.Word[0]
                    print "Place one Checkpoint 2"
                    # self.ASR.unsubscribe("Test_ASR")
                    time.sleep(2)
                    # break

                if self.Word[1] >= 0.400 and self.Word[0] == '五号桌':
                    # self.Navigation.startLocalization()
                    print "Place one Checkpoint 1"
                    # self.Motion.moveTo(0, self.a, 0)
                    self.Motion.moveTo(0.25 * self.x + 0.5 * self.a, 0, 0)
                    self.Motion.moveTo(0, -0.5 * self.b - self.y - self.r, 0)
                    self.Motion.moveTo(self.r + 0.25 * self.x, 0, 0)

                    # self.Motion.moveTo(0, 0, 3.14)
                    # self.Navigation.wait(Moving_Lab1, 1)

                    self.AnimSpeech.say("已到达五号桌，请说点餐来开启服务", self.configuration)
                    self.ASR.unsubscribe("Test_ASR")
                    self.Posture.goToPosture("StandInit", 0.5)
                    self.start = self.Word[0]
                    print "Place one Checkpoint 2"
                    # self.ASR.unsubscribe("Test_ASR")
                    time.sleep(2)
                    # break

                if self.Word[1] >= 0.400 and self.Word[0] == '六号桌':
                    # self.Navigation.startLocalization()
                    print "Place one Checkpoint 1"
                    self.Motion.moveTo(0.5 * self.x + self.a, 0, 0)
                    # self.Navigation.wait(Moving_Lab1, 1)

                    self.AnimSpeech.say("已到达六号桌，请说点餐来开启服务", self.configuration)
                    self.ASR.unsubscribe("Test_ASR")
                    self.Posture.goToPosture("StandInit", 0.5)
                    self.start = self.Word[0]
                    print "Place one Checkpoint 2"
                    # self.ASR.unsubscribe("Test_ASR")
                    time.sleep(2)
                    # break

                if self.Word[1] >= 0.400 and self.Word[0] == '七号桌':
                    # self.Navigation.startLocalization()
                    print "Place one Checkpoint 1"
                    # self.Motion.moveTo(0, self.a, 0)
                    self.Motion.moveTo(0.25 * self.x + 0.5 * self.a, 0, 0)
                    self.Motion.moveTo(0, -0.5 * self.b - self.y - self.r, 0)
                    self.Motion.moveTo(self.r + 0.75 * self.x, 0, 0)

                    # self.Navigation.wait(Moving_Lab1, 1)

                    self.AnimSpeech.say("已到达七号桌，请说点餐来开启服务", self.configuration)
                    self.ASR.unsubscribe("Test_ASR")
                    self.Posture.goToPosture("StandInit", 0.5)
                    self.start = self.Word[0]
                    print "Place one Checkpoint 2"
                    # self.ASR.unsubscribe("Test_ASR")
                    time.sleep(2)
                    # break

                if self.Word[1] >= 0.400 and self.Word[0] == '八号桌':
                    # self.Navigation.startLocalization()
                    print "Place one Checkpoint 1"
                    self.Motion.moveTo(self.x + self.a, 0, 0)

                    # self.Navigation.wait(Moving_Lab1, 1)

                    self.AnimSpeech.say("已到达八号桌，请说点餐来开启服务", self.configuration)
                    self.ASR.unsubscribe("Test_ASR")
                    self.Posture.goToPosture("StandInit", 0.5)
                    self.start = self.Word[0]
                    print "Place one Checkpoint 2"
                    # self.ASR.unsubscribe("Test_ASR")
                    time.sleep(2)
                    # break

                if self.Word[1] >= 0.400 and self.Word[0] == '九号桌':
                    # self.Navigation.startLocalization()
                    print "Place one Checkpoint 1"
                    self.Motion.moveTo(0.25 * self.x + 0.5 * self.a, 0, 0)
                    self.Motion.moveTo(0, self.b + self.y, 0)
                    self.Motion.moveTo(0.5 * self.a + 0.75 * self.x, 0, 0)
                    # self.Navigation.wait(Moving_Lab1, 1)

                    self.AnimSpeech.say("已到达九号桌，请说点餐来开启服务", self.configuration)
                    self.ASR.unsubscribe("Test_ASR")
                    self.Posture.goToPosture("StandInit", 0.5)
                    self.start = self.Word[0]
                    print "Place one Checkpoint 2"
                    # self.ASR.unsubscribe("Test_ASR")
                    time.sleep(2)
                    # break

                if self.Word[1] >= 0.400 and self.Word[0] == '十号桌':
                    # self.Navigation.startLocalization()
                    print "Place one Checkpoint 1"
                    self.Motion.moveTo(0.25 * self.x + 0.5 * self.a, 0, 0)
                    self.Motion.moveTo(0, self.b + self.y, 0)
                    self.Motion.moveTo(-0.5 * self.a - 0.25 * self.x, 0, 0)

                    # self.Navigation.wait(Moving_Lab1, 1)

                    self.AnimSpeech.say("已到达十号桌，请说点餐来开启服务", self.configuration)
                    self.ASR.unsubscribe("Test_ASR")
                    self.Posture.goToPosture("StandInit", 0.5)
                    self.start = self.Word[0]
                    print "Place one Checkpoint 2"
                    # self.ASR.unsubscribe("Test_ASR")
                    time.sleep(2)
                    # break

        elif self.start == "五号桌":
            while True:
                if self.Word[1] >= 0.400 and self.Word[
                    0] == '一号桌':  # Recognitio2n of words and moving to the point after receiving the word input
                    # self.Navigation.startLocalization()
                    print "Place one Checkpoint 1"

                    self.Motion.moveTo(-self.x - self.a, 0, 0)

                    self.AnimSpeech.say("已到达一号桌，请说点餐来开启服务", self.configuration)
                    self.ASR.unsubscribe("Test_ASR")
                    self.Posture.goToPosture("StandInit", 0.5)
                    self.start = self.Word[0]
                    print "Place one Checkpoint 2"
                    # self.ASR.unsubscribe("Test_ASR")
                    time.sleep(2)
                    # break

                if self.Word[1] >= 0.400 and self.Word[0] == '二号桌':
                    # self.Navigation.startLocalization()
                    print "Place one Checkpoint 1"
                    self.Motion.moveTo(-0.25 * self.x - 0.5 * self.a, 0, 0)
                    self.Motion.moveTo(0, self.r + self.y + 0.5 * self.b, 0)
                    self.Motion.moveTo(-0.5 * self.a - 0.75 * self.x, 0, 0)
                    # self.Motion.moveTo(0.5 * self.channel + 0.5 * self.d_Table, 0, 0)
                    # self.Navigation.wait(Moving_Lab1, 1)

                    self.AnimSpeech.say("已到达二号桌，请说点餐来开启服务", self.configuration)
                    self.ASR.unsubscribe("Test_ASR")
                    self.Posture.goToPosture("StandInit", 0.5)
                    self.start = self.Word[0]
                    print "Place one Checkpoint 2"
                    # self.ASR.unsubscribe("Test_ASR")
                    time.sleep(2)
                    # break

                if self.Word[1] >= 0.400 and self.Word[0] == '三号桌':
                    # self.Navigation.startLocalization()
                    print "Place one Checkpoint 1"
                    # self.Motion.moveTo(0, self.a, 0)
                    self.Motion.moveTo(-0.5 * self.x - self.a, 0, 0)
                    # self.Navigation.wait(Moving_Lab1, 1)

                    self.AnimSpeech.say("已到达三号桌，请说点餐来开启服务", self.configuration)
                    self.ASR.unsubscribe("Test_ASR")
                    self.Posture.goToPosture("StandInit", 0.5)
                    self.start = self.Word[0]
                    print "Place one Checkpoint 2"
                    # self.ASR.unsubscribe("Test_ASR")
                    time.sleep(2)
                    # break

                if self.Word[1] >= 0.400 and self.Word[0] == '四号桌':
                    # self.Navigation.startLocalization()
                    print "Place one Checkpoint 1"
                    # self.Motion.moveTo(self.d_Table, 0, 0)
                    self.Motion.moveTo(-0.25 * self.x - 0.5 * self.a, 0, 0)
                    self.Motion.moveTo(0, self.r + self.y + 0.5 * self.b, 0)
                    self.Motion.moveTo(-0.5 * self.a - 0.25 * self.x, 0, 0)
                    # self.Navigation.wait(Moving_Lab1, 1)

                    self.AnimSpeech.say("已到达四号桌，请说点餐来开启服务", self.configuration)
                    self.ASR.unsubscribe("Test_ASR")
                    self.Posture.goToPosture("StandInit", 0.5)
                    self.start = self.Word[0]
                    print "Place one Checkpoint 2"
                    # self.ASR.unsubscribe("Test_ASR")
                    time.sleep(2)
                    # break

                if self.Word[1] >= 0.400 and self.Word[0] == '五号桌':
                    # self.Navigation.startLocalization()
                    print "Place one Checkpoint 1"
                    self.Motion.moveTo(0, 0, 0)
                    # self.Motion.moveTo(self.channel + self.d_Table, 0, 0)
                    # self.Motion.moveTo(0, 0, 3.14)
                    # self.Navigation.wait(Moving_Lab1, 1)

                    self.AnimSpeech.say("已到达五号桌，请说点餐来开启服务", self.configuration)
                    self.ASR.unsubscribe("Test_ASR")
                    self.Posture.goToPosture("StandInit", 0.5)
                    self.start = self.Word[0]
                    print "Place one Checkpoint 2"
                    # self.ASR.unsubscribe("Test_ASR")
                    time.sleep(2)
                    # break

                if self.Word[1] >= 0.400 and self.Word[0] == '六号桌':
                    # self.Navigation.startLocalization()
                    print "Place one Checkpoint 1"
                    # self.Motion.moveTo(self.channel + self.d_Table, 0, 0)
                    self.Motion.moveTo(-0.25 * self.x - 0.5 * self.a, 0, 0)
                    self.Motion.moveTo(0, self.r + self.y + 0.5 * self.b, 0)
                    self.Motion.moveTo(0.5 * self.a + 0.25 * self.x, 0, 0)
                    # self.Navigation.wait(Moving_Lab1, 1)

                    self.AnimSpeech.say("已到达六号桌，请说点餐来开启服务", self.configuration)
                    self.ASR.unsubscribe("Test_ASR")
                    self.Posture.goToPosture("StandInit", 0.5)
                    self.start = self.Word[0]
                    print "Place one Checkpoint 2"
                    # self.ASR.unsubscribe("Test_ASR")
                    time.sleep(2)
                    # break

                if self.Word[1] >= 0.400 and self.Word[0] == '七号桌':
                    # self.Navigation.startLocalization()
                    print "Place one Checkpoint 1"
                    # self.Motion.moveTo(0, self.a, 0)
                    self.Motion.moveTo(0.5 * self.x, 0, 0)
                    # self.Navigation.wait(Moving_Lab1, 1)

                    self.AnimSpeech.say("已到达七号桌，请说点餐来开启服务", self.configuration)
                    self.ASR.unsubscribe("Test_ASR")
                    self.Posture.goToPosture("StandInit", 0.5)
                    self.start = self.Word[0]
                    print "Place one Checkpoint 2"
                    # self.ASR.unsubscribe("Test_ASR")
                    time.sleep(2)
                    # break

                if self.Word[1] >= 0.400 and self.Word[0] == '八号桌':
                    # self.Navigation.startLocalization()
                    print "Place one Checkpoint 1"
                    self.Motion.moveTo(-0.25 * self.x - 0.5 * self.a, 0, 0)
                    self.Motion.moveTo(0, self.r + self.y + 0.5 * self.b, 0)
                    self.Motion.moveTo(0.5 * self.a + 0.75 * self.x, 0, 0)

                    # self.Navigation.wait(Moving_Lab1, 1)

                    self.AnimSpeech.say("已到达八号桌，请说点餐来开启服务", self.configuration)
                    self.ASR.unsubscribe("Test_ASR")
                    self.Posture.goToPosture("StandInit", 0.5)
                    self.start = self.Word[0]
                    print "Place one Checkpoint 2"
                    # self.ASR.unsubscribe("Test_ASR")
                    time.sleep(2)
                    # break

                if self.Word[1] >= 0.400 and self.Word[0] == '九号桌':
                    # self.Navigation.startLocalization()
                    print "Place one Checkpoint 1"
                    self.Motion.moveTo(-0.25 * self.x - 0.5 * self.a, 0, 0)
                    self.Motion.moveTo(0, self.r + 2 * self.y + 1.5 * self.b, 0)
                    self.Motion.moveTo(0.5 * self.a + 0.75 * self.x, 0, 0)
                    # self.Navigation.wait(Moving_Lab1, 1)

                    self.AnimSpeech.say("已到达九号桌，请说点餐来开启服务", self.configuration)
                    self.ASR.unsubscribe("Test_ASR")
                    self.Posture.goToPosture("StandInit", 0.5)
                    self.start = self.Word[0]
                    print "Place one Checkpoint 2"
                    # self.ASR.unsubscribe("Test_ASR")
                    time.sleep(2)
                    # break

                if self.Word[1] >= 0.400 and self.Word[0] == '十号桌':
                    # self.Navigation.startLocalization()
                    print "Place one Checkpoint 1"
                    self.Motion.moveTo(-0.25 * self.x - 0.5 * self.a, 0, 0)
                    self.Motion.moveTo(0, self.r + 2 * self.y + 1.5 * self.b, 0)
                    self.Motion.moveTo(-0.5 * self.a - 0.25 * self.x, 0, 0)

                    # self.Navigation.wait(Moving_Lab1, 1)

                    self.AnimSpeech.say("已到达十号桌，请说点餐来开启服务", self.configuration)
                    self.ASR.unsubscribe("Test_ASR")
                    self.Posture.goToPosture("StandInit", 0.5)
                    self.start = self.Word[0]
                    print "Place one Checkpoint 2"
                    # self.ASR.unsubscribe("Test_ASR")
                    time.sleep(2)
                    # break

        elif self.start == "六号桌":
            while True:
                if self.Word[1] >= 0.400 and self.Word[
                    0] == '一号桌':  # Recognitio2n of words and moving to the point after receiving the word input
                    # self.Navigation.startLocalization()
                    print "Place one Checkpoint 1"

                    self.Motion.moveTo(-0.25 * self.x - 0.5 * self.a, 0, 0)
                    self.Motion.moveTo(0, -0.5 * self.b - self.y - self.r, 0)
                    self.Motion.moveTo(-0.5 * self.a - 0.75 * self.x, 0, 0)

                    self.AnimSpeech.say("已到达一号桌，请说点餐来开启服务", self.configuration)
                    self.ASR.unsubscribe("Test_ASR")
                    self.Posture.goToPosture("StandInit", 0.5)
                    self.start = self.Word[0]
                    print "Place one Checkpoint 2"
                    # self.ASR.unsubscribe("Test_ASR")
                    time.sleep(2)
                    # break

                if self.Word[1] >= 0.400 and self.Word[0] == '二号桌':
                    # self.Navigation.startLocalization()
                    print "Place one Checkpoint 1"
                    self.Motion.moveTo(-self.x - self.a, 0, 0)
                    # self.Motion.moveTo(0.5 * self.channel + 0.5 * self.d_Table, 0, 0)
                    # self.Navigation.wait(Moving_Lab1, 1)

                    self.AnimSpeech.say("已到达二号桌，请说点餐来开启服务", self.configuration)
                    self.ASR.unsubscribe("Test_ASR")
                    self.Posture.goToPosture("StandInit", 0.5)
                    self.start = self.Word[0]
                    print "Place one Checkpoint 2"
                    # self.ASR.unsubscribe("Test_ASR")
                    time.sleep(2)
                    # break

                if self.Word[1] >= 0.400 and self.Word[0] == '三号桌':
                    # self.Navigation.startLocalization()
                    print "Place one Checkpoint 1"
                    self.Motion.moveTo(-0.25 * self.x - 0.5 * self.a, 0, 0)
                    self.Motion.moveTo(0, -0.5 * self.b - self.y - self.r, 0)
                    self.Motion.moveTo(-0.5 * self.a - 0.25 * self.x, 0, 0)

                    # self.Navigation.wait(Moving_Lab1, 1)

                    self.AnimSpeech.say("已到达三号桌，请说点餐来开启服务", self.configuration)
                    self.ASR.unsubscribe("Test_ASR")
                    self.Posture.goToPosture("StandInit", 0.5)
                    self.start = self.Word[0]
                    print "Place one Checkpoint 2"
                    # self.ASR.unsubscribe("Test_ASR")
                    time.sleep(2)
                    # break

                if self.Word[1] >= 0.400 and self.Word[0] == '四号桌':
                    # self.Navigation.startLocalization()
                    print "Place one Checkpoint 1"
                    # self.Motion.moveTo(self.d_Table, 0, 0)
                    # self.Navigation.wait(Moving_Lab1, 1)
                    self.Motion.moveTo(-0.5 * self.x - self.a, 0, 0)

                    self.AnimSpeech.say("已到达四号桌，请说点餐来开启服务", self.configuration)
                    self.ASR.unsubscribe("Test_ASR")
                    self.Posture.goToPosture("StandInit", 0.5)
                    self.start = self.Word[0]
                    print "Place one Checkpoint 2"
                    # self.ASR.unsubscribe("Test_ASR")
                    time.sleep(2)
                    # break

                if self.Word[1] >= 0.400 and self.Word[0] == '五号桌':
                    # self.Navigation.startLocalization()
                    print "Place one Checkpoint 1"
                    # self.Motion.moveTo(0, self.a, 0)
                    # self.Motion.moveTo(self.channel + self.d_Table, 0, 0)
                    self.Motion.moveTo(-0.25 * self.x - 0.5 * self.a, 0, 0)
                    self.Motion.moveTo(0, -0.5 * self.b - self.y - self.r, 0)
                    self.Motion.moveTo(0.5 * self.a + 0.25 * self.x, 0, 0)
                    # self.Motion.moveTo(0, 0, 3.14)
                    # self.Navigation.wait(Moving_Lab1, 1)

                    self.AnimSpeech.say("已到达五号桌，请说点餐来开启服务", self.configuration)
                    self.ASR.unsubscribe("Test_ASR")
                    self.Posture.goToPosture("StandInit", 0.5)
                    self.start = self.Word[0]
                    print "Place one Checkpoint 2"
                    # self.ASR.unsubscribe("Test_ASR")
                    time.sleep(2)
                    # break

                if self.Word[1] >= 0.400 and self.Word[0] == '六号桌':
                    # self.Navigation.startLocalization()
                    print "Place one Checkpoint 1"
                    self.Motion.moveTo(0, 0, 0)
                    # self.Navigation.wait(Moving_Lab1, 1)

                    self.AnimSpeech.say("已到达六号桌，请说点餐来开启服务", self.configuration)
                    self.ASR.unsubscribe("Test_ASR")
                    self.Posture.goToPosture("StandInit", 0.5)
                    self.start = self.Word[0]
                    print "Place one Checkpoint 2"
                    # self.ASR.unsubscribe("Test_ASR")
                    time.sleep(2)
                    # break

                if self.Word[1] >= 0.400 and self.Word[0] == '七号桌':
                    # self.Navigation.startLocalization()
                    print "Place one Checkpoint 1"
                    # self.Motion.moveTo(0, self.a, 0)
                    self.Motion.moveTo(-0.25 * self.x - 0.5 * self.a, 0, 0)
                    self.Motion.moveTo(0, -0.5 * self.b - self.y - self.r, 0)
                    self.Motion.moveTo(0.5 * self.a + 0.75 * self.x, 0, 0)

                    # self.Navigation.wait(Moving_Lab1, 1)

                    self.AnimSpeech.say("已到达七号桌，请说点餐来开启服务", self.configuration)
                    self.ASR.unsubscribe("Test_ASR")
                    self.Posture.goToPosture("StandInit", 0.5)
                    self.start = self.Word[0]
                    print "Place one Checkpoint 2"
                    # self.ASR.unsubscribe("Test_ASR")
                    time.sleep(2)
                    # break

                if self.Word[1] >= 0.400 and self.Word[0] == '八号桌':
                    # self.Navigation.startLocalization()
                    print "Place one Checkpoint 1"
                    self.Motion.moveTo(0.5 * self.x, 0, 0)

                    # self.Navigation.wait(Moving_Lab1, 1)

                    self.AnimSpeech.say("已到达八号桌，请说点餐来开启服务", self.configuration)
                    self.ASR.unsubscribe("Test_ASR")
                    self.Posture.goToPosture("StandInit", 0.5)
                    self.start = self.Word[0]
                    print "Place one Checkpoint 2"
                    # self.ASR.unsubscribe("Test_ASR")
                    time.sleep(2)
                    # break

                if self.Word[1] >= 0.400 and self.Word[0] == '九号桌':
                    # self.Navigation.startLocalization()
                    print "Place one Checkpoint 1"
                    self.Motion.moveTo(-0.25 * self.x - 0.5 * self.a, 0, 0)
                    self.Motion.moveTo(0, self.b + self.y, 0)
                    self.Motion.moveTo(0.5 * self.a + 0.75 * self.x, 0, 0)
                    # self.Navigation.wait(Moving_Lab1, 1)

                    self.AnimSpeech.say("已到达九号桌，请说点餐来开启服务", self.configuration)
                    self.ASR.unsubscribe("Test_ASR")
                    self.Posture.goToPosture("StandInit", 0.5)
                    self.start = self.Word[0]
                    print "Place one Checkpoint 2"
                    # self.ASR.unsubscribe("Test_ASR")
                    time.sleep(2)
                    # break

                if self.Word[1] >= 0.400 and self.Word[0] == '十号桌':
                    # self.Navigation.startLocalization()
                    print "Place one Checkpoint 1"
                    self.Motion.moveTo(-0.25 * self.x - 0.5 * self.a, 0, 0)
                    self.Motion.moveTo(0, self.b + self.y, 0)
                    self.Motion.moveTo(-0.5 * self.a - 0.25 * self.x, 0, 0)

                    # self.Navigation.wait(Moving_Lab1, 1)

                    self.AnimSpeech.say("已到达十号桌，请说点餐来开启服务", self.configuration)
                    self.ASR.unsubscribe("Test_ASR")
                    self.Posture.goToPosture("StandInit", 0.5)
                    self.start = self.Word[0]
                    print "Place one Checkpoint 2"
                    # self.ASR.unsubscribe("Test_ASR")
                    time.sleep(2)
                    # break


        elif self.start == "七号桌":
            while True:
                if self.Word[1] >= 0.400 and self.Word[
                    0] == '一号桌':  # Recognitio2n of words and moving to the point after receiving the word input
                    # self.Navigation.startLocalization()
                    print "Place one Checkpoint 1"

                    self.Motion.moveTo(-1.5 * self.x - self.a, 0, 0)

                    self.AnimSpeech.say("已到达一号桌，请说点餐来开启服务", self.configuration)
                    self.ASR.unsubscribe("Test_ASR")
                    self.Posture.goToPosture("StandInit", 0.5)
                    self.start = self.Word[0]
                    print "Place one Checkpoint 2"
                    # self.ASR.unsubscribe("Test_ASR")
                    time.sleep(2)
                    # break

                if self.Word[1] >= 0.400 and self.Word[0] == '二号桌':
                    # self.Navigation.startLocalization()
                    print "Place one Checkpoint 1"
                    self.Motion.moveTo(-0.75 * self.x - 0.5 * self.a, 0, 0)
                    self.Motion.moveTo(0, self.r + self.y + 0.5 * self.b, 0)
                    self.Motion.moveTo(-0.5 * self.a - 0.75 * self.x, 0, 0)
                    # self.Motion.moveTo(0.5 * self.channel + 0.5 * self.d_Table, 0, 0)
                    # self.Navigation.wait(Moving_Lab1, 1)

                    self.AnimSpeech.say("已到达二号桌，请说点餐来开启服务", self.configuration)
                    self.ASR.unsubscribe("Test_ASR")
                    self.Posture.goToPosture("StandInit", 0.5)
                    self.start = self.Word[0]
                    print "Place one Checkpoint 2"
                    # self.ASR.unsubscribe("Test_ASR")
                    time.sleep(2)
                    # break

                if self.Word[1] >= 0.400 and self.Word[0] == '三号桌':
                    # self.Navigation.startLocalization()
                    print "Place one Checkpoint 1"
                    # self.Motion.moveTo(0, self.a, 0)
                    self.Motion.moveTo(-self.x - self.a, 0, 0)
                    # self.Navigation.wait(Moving_Lab1, 1)

                    self.AnimSpeech.say("已到达三号桌，请说点餐来开启服务", self.configuration)
                    self.ASR.unsubscribe("Test_ASR")
                    self.Posture.goToPosture("StandInit", 0.5)
                    self.start = self.Word[0]
                    print "Place one Checkpoint 2"
                    # self.ASR.unsubscribe("Test_ASR")
                    time.sleep(2)
                    # break

                if self.Word[1] >= 0.400 and self.Word[0] == '四号桌':
                    # self.Navigation.startLocalization()
                    print "Place one Checkpoint 1"
                    # self.Motion.moveTo(self.d_Table, 0, 0)
                    self.Motion.moveTo(-0.75 * self.x - 0.5 * self.a, 0, 0)
                    self.Motion.moveTo(0, self.r + self.y + 0.5 * self.b, 0)
                    self.Motion.moveTo(-0.5 * self.a - 0.25 * self.x, 0, 0)
                    # self.Navigation.wait(Moving_Lab1, 1)

                    self.AnimSpeech.say("已到达四号桌，请说点餐来开启服务", self.configuration)
                    self.ASR.unsubscribe("Test_ASR")
                    self.Posture.goToPosture("StandInit", 0.5)
                    self.start = self.Word[0]
                    print "Place one Checkpoint 2"
                    # self.ASR.unsubscribe("Test_ASR")
                    time.sleep(2)
                    # break

                if self.Word[1] >= 0.400 and self.Word[0] == '五号桌':
                    # self.Navigation.startLocalization()
                    print "Place one Checkpoint 1"
                    self.Motion.moveTo(-0.5 * self.x, 0, 0)
                    # self.Motion.moveTo(0, 0, 0)
                    # self.Motion.moveTo(self.channel + self.d_Table, 0, 0)
                    # self.Motion.moveTo(0, 0, 3.14)
                    # self.Navigation.wait(Moving_Lab1, 1)

                    self.AnimSpeech.say("已到达五号桌，请说点餐来开启服务", self.configuration)
                    self.ASR.unsubscribe("Test_ASR")
                    self.Posture.goToPosture("StandInit", 0.5)
                    self.start = self.Word[0]
                    print "Place one Checkpoint 2"
                    # self.ASR.unsubscribe("Test_ASR")
                    time.sleep(2)
                    # break

                if self.Word[1] >= 0.400 and self.Word[0] == '六号桌':
                    # self.Navigation.startLocalization()
                    print "Place one Checkpoint 1"
                    self.Motion.moveTo(-0.75 * self.x - 0.5 * self.a, 0, 0)
                    self.Motion.moveTo(0, self.r + self.y + 0.5 * self.b, 0)
                    self.Motion.moveTo(0.5 * self.a + 0.25 * self.x, 0, 0)
                    # self.Navigation.wait(Moving_Lab1, 1)

                    self.AnimSpeech.say("已到达六号桌，请说点餐来开启服务", self.configuration)
                    self.ASR.unsubscribe("Test_ASR")
                    self.Posture.goToPosture("StandInit", 0.5)
                    self.start = self.Word[0]
                    print "Place one Checkpoint 2"
                    # self.ASR.unsubscribe("Test_ASR")
                    time.sleep(2)
                    # break

                if self.Word[1] >= 0.400 and self.Word[0] == '七号桌':
                    # self.Navigation.startLocalization()
                    print "Place one Checkpoint 1"
                    # self.Motion.moveTo(0, self.a, 0)
                    self.Motion.moveTo(0, 0, 0)
                    # self.Navigation.wait(Moving_Lab1, 1)

                    self.AnimSpeech.say("已到达七号桌，请说点餐来开启服务", self.configuration)
                    self.ASR.unsubscribe("Test_ASR")
                    self.Posture.goToPosture("StandInit", 0.5)
                    self.start = self.Word[0]
                    print "Place one Checkpoint 2"
                    # self.ASR.unsubscribe("Test_ASR")
                    time.sleep(2)
                    # break

                if self.Word[1] >= 0.400 and self.Word[0] == '八号桌':
                    # self.Navigation.startLocalization()
                    print "Place one Checkpoint 1"
                    # self.Motion.moveTo(self.d_Table, 0, 0)
                    self.Motion.moveTo(-0.75 * self.x - 0.5 * self.a, 0, 0)
                    self.Motion.moveTo(0, self.r + self.y + 0.5 * self.b, 0)
                    self.Motion.moveTo(0.5 * self.a + 0.75 * self.x, 0, 0)

                    # self.Navigation.wait(Moving_Lab1, 1)

                    self.AnimSpeech.say("已到达八号桌，请说点餐来开启服务", self.configuration)
                    self.ASR.unsubscribe("Test_ASR")
                    self.Posture.goToPosture("StandInit", 0.5)
                    self.start = self.Word[0]
                    print "Place one Checkpoint 2"
                    # self.ASR.unsubscribe("Test_ASR")
                    time.sleep(2)
                    # break

                if self.Word[1] >= 0.400 and self.Word[0] == '九号桌':
                    # self.Navigation.startLocalization()
                    print "Place one Checkpoint 1"
                    self.Motion.moveTo(-0.75 * self.x - 0.5 * self.a, 0, 0)
                    self.Motion.moveTo(0, self.r + 2 * self.y + 1.5 * self.b, 0)
                    self.Motion.moveTo(0.5 * self.a + 0.75 * self.x, 0, 0)
                    # self.Navigation.wait(Moving_Lab1, 1)

                    self.AnimSpeech.say("已到达九号桌，请说点餐来开启服务", self.configuration)
                    self.ASR.unsubscribe("Test_ASR")
                    self.Posture.goToPosture("StandInit", 0.5)
                    self.start = self.Word[0]
                    print "Place one Checkpoint 2"
                    # self.ASR.unsubscribe("Test_ASR")
                    time.sleep(2)
                    # break

                if self.Word[1] >= 0.400 and self.Word[0] == '十号桌':
                    # self.Navigation.startLocalization()
                    print "Place one Checkpoint 1"
                    self.Motion.moveTo(-0.75 * self.x - 0.5 * self.a, 0, 0)
                    self.Motion.moveTo(0, self.r + 2 * self.y + 1.5 * self.b, 0)
                    self.Motion.moveTo(-0.5 * self.a - 0.25 * self.x, 0, 0)

                    # self.Navigation.wait(Moving_Lab1, 1)

                    self.AnimSpeech.say("已到达十号桌，请说点餐来开启服务", self.configuration)
                    self.ASR.unsubscribe("Test_ASR")
                    self.Posture.goToPosture("StandInit", 0.5)
                    self.start = self.Word[0]
                    print "Place one Checkpoint 2"
                    # self.ASR.unsubscribe("Test_ASR")
                    time.sleep(2)
                    # break


        elif self.start == "八号桌":
            while True:
                if self.Word[1] >= 0.400 and self.Word[
                    0] == '一号桌':  # Recognitio2n of words and moving to the point after receiving the word input
                    # self.Navigation.startLocalization()
                    print "Place one Checkpoint 1"

                    self.Motion.moveTo(-0.75 * self.x - 0.5 * self.a, 0, 0)
                    self.Motion.moveTo(0, -0.5 * self.b - self.y - self.r, 0)
                    self.Motion.moveTo(-0.5 * self.a - 0.75 * self.x, 0, 0)

                    self.AnimSpeech.say("已到达一号桌，请说点餐来开启服务", self.configuration)
                    self.ASR.unsubscribe("Test_ASR")
                    self.Posture.goToPosture("StandInit", 0.5)
                    self.start = self.Word[0]
                    print "Place one Checkpoint 2"
                    # self.ASR.unsubscribe("Test_ASR")
                    time.sleep(2)
                    # break

                if self.Word[1] >= 0.400 and self.Word[0] == '二号桌':
                    # self.Navigation.startLocalization()
                    print "Place one Checkpoint 1"
                    self.Motion.moveTo(-1.5 * self.x - self.a, 0, 0)
                    # self.Motion.moveTo(0.5 * self.channel + 0.5 * self.d_Table, 0, 0)
                    # self.Navigation.wait(Moving_Lab1, 1)

                    self.AnimSpeech.say("已到达二号桌，请说点餐来开启服务", self.configuration)
                    self.ASR.unsubscribe("Test_ASR")
                    self.Posture.goToPosture("StandInit", 0.5)
                    self.start = self.Word[0]
                    print "Place one Checkpoint 2"
                    # self.ASR.unsubscribe("Test_ASR")
                    time.sleep(2)
                    # break

                if self.Word[1] >= 0.400 and self.Word[0] == '三号桌':
                    # self.Navigation.startLocalization()
                    print "Place one Checkpoint 1"
                    # self.Motion.moveTo(0, self.a, 0)
                    self.Motion.moveTo(-0.75 * self.x - 0.5 * self.a, 0, 0)
                    self.Motion.moveTo(0, -0.5 * self.b - self.y - self.r, 0)
                    self.Motion.moveTo(-0.5 * self.a - 0.25 * self.x, 0, 0)

                    # self.Navigation.wait(Moving_Lab1, 1)

                    self.AnimSpeech.say("已到达三号桌，请说点餐来开启服务", self.configuration)
                    self.ASR.unsubscribe("Test_ASR")
                    self.Posture.goToPosture("StandInit", 0.5)
                    self.start = self.Word[0]
                    print "Place one Checkpoint 2"
                    # self.ASR.unsubscribe("Test_ASR")
                    time.sleep(2)
                    # break

                if self.Word[1] >= 0.400 and self.Word[0] == '四号桌':
                    # self.Navigation.startLocalization()
                    print "Place one Checkpoint 1"
                    # self.Motion.moveTo(self.d_Table, 0, 0)
                    self.Motion.moveTo(-self.x - self.a, 0, 0)
                    # self.Navigation.wait(Moving_Lab1, 1)

                    self.AnimSpeech.say("已到达四号桌，请说点餐来开启服务", self.configuration)
                    self.ASR.unsubscribe("Test_ASR")
                    self.Posture.goToPosture("StandInit", 0.5)
                    self.start = self.Word[0]
                    print "Place one Checkpoint 2"
                    # self.ASR.unsubscribe("Test_ASR")
                    time.sleep(2)
                    # break

                if self.Word[1] >= 0.400 and self.Word[0] == '五号桌':
                    # self.Navigation.startLocalization()
                    print "Place one Checkpoint 1"
                    self.Motion.moveTo(-0.75 * self.x - 0.5 * self.a, 0, 0)
                    self.Motion.moveTo(0, -0.5 * self.b - self.y - self.r, 0)
                    self.Motion.moveTo(0.5 * self.a + 0.25 * self.x, 0, 0)

                    # self.Motion.moveTo(0, 0, 0)
                    # self.Motion.moveTo(self.channel + self.d_Table, 0, 0)
                    # self.Motion.moveTo(0, 0, 3.14)
                    # self.Navigation.wait(Moving_Lab1, 1)

                    self.AnimSpeech.say("已到达五号桌，请说点餐来开启服务", self.configuration)
                    self.ASR.unsubscribe("Test_ASR")
                    self.Posture.goToPosture("StandInit", 0.5)
                    self.start = self.Word[0]
                    print "Place one Checkpoint 2"
                    # self.ASR.unsubscribe("Test_ASR")
                    time.sleep(2)
                    # break

                if self.Word[1] >= 0.400 and self.Word[0] == '六号桌':
                    # self.Navigation.startLocalization()
                    print "Place one Checkpoint 1"
                    self.Motion.moveTo(-0.5 * self.x, 0, 0)
                    # self.Navigation.wait(Moving_Lab1, 1)

                    self.AnimSpeech.say("已到达六号桌，请说点餐来开启服务", self.configuration)
                    self.ASR.unsubscribe("Test_ASR")
                    self.Posture.goToPosture("StandInit", 0.5)
                    self.start = self.Word[0]
                    print "Place one Checkpoint 2"
                    # self.ASR.unsubscribe("Test_ASR")
                    time.sleep(2)
                    # break

                if self.Word[1] >= 0.400 and self.Word[0] == '七号桌':
                    # self.Navigation.startLocalization()
                    print "Place one Checkpoint 1"
                    # self.Motion.moveTo(0, self.a, 0)
                    self.Motion.moveTo(-0.75 * self.x - 0.5 * self.a, 0, 0)
                    self.Motion.moveTo(0, -0.5 * self.b - self.y - self.r, 0)
                    self.Motion.moveTo(0.5 * self.a + 0.75 * self.x, 0, 0)

                    # self.Navigation.wait(Moving_Lab1, 1)

                    self.AnimSpeech.say("已到达七号桌，请说点餐来开启服务", self.configuration)
                    self.ASR.unsubscribe("Test_ASR")
                    self.Posture.goToPosture("StandInit", 0.5)
                    self.start = self.Word[0]
                    print "Place one Checkpoint 2"
                    # self.ASR.unsubscribe("Test_ASR")
                    time.sleep(2)
                    # break

                if self.Word[1] >= 0.400 and self.Word[0] == '八号桌':
                    # self.Navigation.startLocalization()
                    print "Place one Checkpoint 1"
                    # self.Motion.moveTo(self.d_Table, 0, 0)

                    # self.Navigation.wait(Moving_Lab1, 1)

                    self.AnimSpeech.say("已到达八号桌，请说点餐来开启服务", self.configuration)
                    self.ASR.unsubscribe("Test_ASR")
                    self.Posture.goToPosture("StandInit", 0.5)
                    self.start = self.Word[0]
                    print "Place one Checkpoint 2"
                    # self.ASR.unsubscribe("Test_ASR")
                    time.sleep(2)
                    # break

                if self.Word[1] >= 0.400 and self.Word[0] == '九号桌':
                    # self.Navigation.startLocalization()
                    print "Place one Checkpoint 1"
                    self.Motion.moveTo(-0.75 * self.x - 0.5 * self.a, 0, 0)
                    self.Motion.moveTo(0, self.b + self.y, 0)
                    self.Motion.moveTo(0.5 * self.a + 0.75 * self.x, 0, 0)
                    # self.Navigation.wait(Moving_Lab1, 1)

                    self.AnimSpeech.say("已到达九号桌，请说点餐来开启服务", self.configuration)
                    self.ASR.unsubscribe("Test_ASR")
                    self.Posture.goToPosture("StandInit", 0.5)
                    self.start = self.Word[0]
                    print "Place one Checkpoint 2"
                    # self.ASR.unsubscribe("Test_ASR")
                    time.sleep(2)
                    # break

                if self.Word[1] >= 0.400 and self.Word[0] == '十号桌':
                    # self.Navigation.startLocalization()
                    print "Place one Checkpoint 1"
                    self.Motion.moveTo(-0.75 * self.x - 0.5 * self.a, 0, 0)
                    self.Motion.moveTo(0, self.b + self.y, 0)
                    self.Motion.moveTo(-0.5 * self.a - 0.25 * self.x, 0, 0)

                    # self.Navigation.wait(Moving_Lab1, 1)

                    self.AnimSpeech.say("已到达十号桌，请说点餐来开启服务", self.configuration)
                    self.ASR.unsubscribe("Test_ASR")
                    self.Posture.goToPosture("StandInit", 0.5)
                    self.start = self.Word[0]
                    print "Place one Checkpoint 2"
                    # self.ASR.unsubscribe("Test_ASR")
                    time.sleep(2)
                    # break

        elif self.start == "九号桌":
            while True:
                if self.Word[1] >= 0.400 and self.Word[
                    0] == '一号桌':  # Recognitio2n of words and moving to the point after receiving the word input
                    # self.Navigation.startLocalization()
                    print "Place one Checkpoint 1"

                    self.Motion.moveTo(-0.75 * self.x - 0.5 * self.a, 0, 0)
                    self.Motion.moveTo(0, -1.5 * self.b - 2 * self.y - self.r, 0)
                    self.Motion.moveTo(-0.5 * self.a - 0.75 * self.x, 0, 0)

                    self.AnimSpeech.say("已到达一号桌，请说点餐来开启服务", self.configuration)
                    self.ASR.unsubscribe("Test_ASR")
                    self.Posture.goToPosture("StandInit", 0.5)
                    self.start = self.Word[0]
                    print "Place one Checkpoint 2"
                    # self.ASR.unsubscribe("Test_ASR")
                    time.sleep(2)
                    # break

                if self.Word[1] >= 0.400 and self.Word[0] == '二号桌':
                    # self.Navigation.startLocalization()
                    print "Place one Checkpoint 1"
                    self.Motion.moveTo(-0.75 * self.x - 0.5 * self.a, 0, 0)
                    self.Motion.moveTo(0, -self.b - self.y, 0)
                    self.Motion.moveTo(-0.5 * self.a - 0.75 * self.x, 0, 0)
                    # self.Motion.moveTo(0.5 * self.channel + 0.5 * self.d_Table, 0, 0)
                    # self.Navigation.wait(Moving_Lab1, 1)

                    self.AnimSpeech.say("已到达二号桌，请说点餐来开启服务", self.configuration)
                    self.ASR.unsubscribe("Test_ASR")
                    self.Posture.goToPosture("StandInit", 0.5)
                    self.start = self.Word[0]
                    print "Place one Checkpoint 2"
                    # self.ASR.unsubscribe("Test_ASR")
                    time.sleep(2)
                    # break

                if self.Word[1] >= 0.400 and self.Word[0] == '三号桌':
                    # self.Navigation.startLocalization()
                    print "Place one Checkpoint 1"
                    # self.Motion.moveTo(0, self.a, 0)
                    self.Motion.moveTo(-0.75 * self.x - 0.5 * self.a, 0, 0)
                    self.Motion.moveTo(0, -1.5 * self.b - 2 * self.y - self.r, 0)
                    self.Motion.moveTo(-0.5 * self.a - 0.25 * self.x, 0, 0)

                    # self.Navigation.wait(Moving_Lab1, 1)

                    self.AnimSpeech.say("已到达三号桌，请说点餐来开启服务", self.configuration)
                    self.ASR.unsubscribe("Test_ASR")
                    self.Posture.goToPosture("StandInit", 0.5)
                    self.start = self.Word[0]
                    print "Place one Checkpoint 2"
                    # self.ASR.unsubscribe("Test_ASR")
                    time.sleep(2)
                    # break

                if self.Word[1] >= 0.400 and self.Word[0] == '四号桌':
                    # self.Navigation.startLocalization()
                    print "Place one Checkpoint 1"
                    # self.Motion.moveTo(self.d_Table, 0, 0)
                    self.Motion.moveTo(-0.75 * self.x - 0.5 * self.a, 0, 0)
                    self.Motion.moveTo(0, -self.b - self.y, 0)
                    self.Motion.moveTo(-0.5 * self.a - 0.25 * self.x, 0, 0)
                    # self.Navigation.wait(Moving_Lab1, 1)

                    self.AnimSpeech.say("已到达四号桌，请说点餐来开启服务", self.configuration)
                    self.ASR.unsubscribe("Test_ASR")
                    self.Posture.goToPosture("StandInit", 0.5)
                    self.start = self.Word[0]
                    print "Place one Checkpoint 2"
                    # self.ASR.unsubscribe("Test_ASR")
                    time.sleep(2)
                    # break

                if self.Word[1] >= 0.400 and self.Word[0] == '五号桌':
                    # self.Navigation.startLocalization()
                    print "Place one Checkpoint 1"
                    self.Motion.moveTo(-0.75 * self.x - 0.5 * self.a, 0, 0)
                    self.Motion.moveTo(0, -1.5 * self.b - 2 * self.y - self.r, 0)
                    self.Motion.moveTo(0.5 * self.a + 0.25 * self.x, 0, 0)

                    # self.Motion.moveTo(0, 0, 0)
                    # self.Motion.moveTo(self.channel + self.d_Table, 0, 0)
                    # self.Motion.moveTo(0, 0, 3.14)
                    # self.Navigation.wait(Moving_Lab1, 1)

                    self.AnimSpeech.say("已到达五号桌，请说点餐来开启服务", self.configuration)
                    self.ASR.unsubscribe("Test_ASR")
                    self.Posture.goToPosture("StandInit", 0.5)
                    self.start = self.Word[0]
                    print "Place one Checkpoint 2"
                    # self.ASR.unsubscribe("Test_ASR")
                    time.sleep(2)
                    # break

                if self.Word[1] >= 0.400 and self.Word[0] == '六号桌':
                    # self.Navigation.startLocalization()
                    print "Place one Checkpoint 1"
                    self.Motion.moveTo(-0.75 * self.x - 0.5 * self.a, 0, 0)
                    self.Motion.moveTo(0, -self.b - self.y, 0)
                    self.Motion.moveTo(0.5 * self.a + 0.25 * self.x, 0, 0)
                    # self.Navigation.wait(Moving_Lab1, 1)

                    self.AnimSpeech.say("已到达六号桌，请说点餐来开启服务", self.configuration)
                    self.ASR.unsubscribe("Test_ASR")
                    self.Posture.goToPosture("StandInit", 0.5)
                    self.start = self.Word[0]
                    print "Place one Checkpoint 2"
                    # self.ASR.unsubscribe("Test_ASR")
                    time.sleep(2)
                    # break

                if self.Word[1] >= 0.400 and self.Word[0] == '七号桌':
                    # self.Navigation.startLocalization()
                    print "Place one Checkpoint 1"
                    # self.Motion.moveTo(0, self.a, 0)
                    self.Motion.moveTo(-0.75 * self.x - 0.5 * self.a, 0, 0)
                    self.Motion.moveTo(0, -1.5 * self.b - 2 * self.y - self.r, 0)
                    self.Motion.moveTo(0.5 * self.a + 0.75 * self.x, 0, 0)

                    # self.Navigation.wait(Moving_Lab1, 1)

                    self.AnimSpeech.say("已到达七号桌，请说点餐来开启服务", self.configuration)
                    self.ASR.unsubscribe("Test_ASR")
                    self.Posture.goToPosture("StandInit", 0.5)
                    self.start = self.Word[0]
                    print "Place one Checkpoint 2"
                    # self.ASR.unsubscribe("Test_ASR")
                    time.sleep(2)
                    # break

                if self.Word[1] >= 0.400 and self.Word[0] == '八号桌':
                    # self.Navigation.startLocalization()
                    print "Place one Checkpoint 1"
                    self.Motion.moveTo(-0.75 * self.x - 0.5 * self.a, 0, 0)
                    self.Motion.moveTo(0, -self.b - self.y, 0)
                    self.Motion.moveTo(0.5 * self.a + 0.75 * self.x, 0, 0)
                    # self.Navigation.wait(Moving_Lab1, 1)

                    self.AnimSpeech.say("已到达八号桌，请说点餐来开启服务", self.configuration)
                    self.ASR.unsubscribe("Test_ASR")
                    self.Posture.goToPosture("StandInit", 0.5)
                    self.start = self.Word[0]
                    print "Place one Checkpoint 2"
                    # self.ASR.unsubscribe("Test_ASR")
                    time.sleep(2)
                    # break

                if self.Word[1] >= 0.400 and self.Word[0] == '九号桌':
                    # self.Navigation.startLocalization()
                    print "Place one Checkpoint 1"
                    self.Motion.moveTo(0, 0, 0)

                    # self.Navigation.wait(Moving_Lab1, 1)

                    self.AnimSpeech.say("已到达九号桌，请说点餐来开启服务", self.configuration)
                    self.ASR.unsubscribe("Test_ASR")
                    self.Posture.goToPosture("StandInit", 0.5)
                    self.start = self.Word[0]
                    print "Place one Checkpoint 2"
                    # self.ASR.unsubscribe("Test_ASR")
                    time.sleep(2)
                    # break

                if self.Word[1] >= 0.400 and self.Word[0] == '十号桌':
                    # self.Navigation.startLocalization()
                    print "Place one Checkpoint 1"
                    self.Motion.moveTo(-self.x - self.a, 0, 0)

                    # self.Navigation.wait(Moving_Lab1, 1)

                    self.AnimSpeech.say("已到达十号桌，请说点餐来开启服务", self.configuration)
                    self.ASR.unsubscribe("Test_ASR")
                    self.Posture.goToPosture("StandInit", 0.5)
                    self.start = self.Word[0]
                    print "Place one Checkpoint 2"
                    # self.ASR.unsubscribe("Test_ASR")
                    time.sleep(2)
                    # break


        elif self.start == "十号桌":
            while True:
                if self.Word[1] >= 0.400 and self.Word[
                    0] == '一号桌':  # Recognitio2n of words and moving to the point after receiving the word input
                    # self.Navigation.startLocalization()
                    print "Place one Checkpoint 1"

                    self.Motion.moveTo(0.25 * self.x + 0.5 * self.a, 0, 0)
                    self.Motion.moveTo(0, -1.5 * self.b - 2 * self.y - self.r, 0)
                    self.Motion.moveTo(-0.5 * self.a - 0.75 * self.x, 0, 0)

                    self.AnimSpeech.say("已到达一号桌，请说点餐来开启服务", self.configuration)
                    self.ASR.unsubscribe("Test_ASR")
                    self.Posture.goToPosture("StandInit", 0.5)
                    self.start = self.Word[0]
                    print "Place one Checkpoint 2"
                    # self.ASR.unsubscribe("Test_ASR")
                    time.sleep(2)
                    # break

                if self.Word[1] >= 0.400 and self.Word[0] == '二号桌':
                    # self.Navigation.startLocalization()
                    print "Place one Checkpoint 1"
                    self.Motion.moveTo(0.25 * self.x + 0.5 * self.a, 0, 0)
                    self.Motion.moveTo(0, -self.b - self.y, 0)
                    self.Motion.moveTo(-0.5 * self.a - 0.75 * self.x, 0, 0)
                    # self.Motion.moveTo(0.5 * self.channel + 0.5 * self.d_Table, 0, 0)
                    # self.Navigation.wait(Moving_Lab1, 1)

                    self.AnimSpeech.say("已到达二号桌，请说点餐来开启服务", self.configuration)
                    self.ASR.unsubscribe("Test_ASR")
                    self.Posture.goToPosture("StandInit", 0.5)
                    self.start = self.Word[0]
                    print "Place one Checkpoint 2"
                    # self.ASR.unsubscribe("Test_ASR")
                    time.sleep(2)
                    # break

                if self.Word[1] >= 0.400 and self.Word[0] == '三号桌':
                    # self.Navigation.startLocalization()
                    print "Place one Checkpoint 1"
                    # self.Motion.moveTo(0, self.a, 0)
                    self.Motion.moveTo(0.25 * self.x + 0.5 * self.a, 0, 0)
                    self.Motion.moveTo(0, -1.5 * self.b - 2 * self.y - self.r, 0)
                    self.Motion.moveTo(-0.5 * self.a - 0.25 * self.x, 0, 0)

                    # self.Navigation.wait(Moving_Lab1, 1)

                    self.AnimSpeech.say("已到达三号桌，请说点餐来开启服务", self.configuration)
                    self.ASR.unsubscribe("Test_ASR")
                    self.Posture.goToPosture("StandInit", 0.5)
                    self.start = self.Word[0]
                    print "Place one Checkpoint 2"
                    # self.ASR.unsubscribe("Test_ASR")
                    time.sleep(2)
                    # break

                if self.Word[1] >= 0.400 and self.Word[0] == '四号桌':
                    # self.Navigation.startLocalization()
                    print "Place one Checkpoint 1"
                    # self.Motion.moveTo(self.d_Table, 0, 0)
                    self.Motion.moveTo(0.25 * self.x + 0.5 * self.a, 0, 0)
                    self.Motion.moveTo(0, -self.b - self.y, 0)
                    self.Motion.moveTo(-0.5 * self.a - 0.25 * self.x, 0, 0)
                    # self.Navigation.wait(Moving_Lab1, 1)

                    self.AnimSpeech.say("已到达四号桌，请说点餐来开启服务", self.configuration)
                    self.ASR.unsubscribe("Test_ASR")
                    self.Posture.goToPosture("StandInit", 0.5)
                    self.start = self.Word[0]
                    print "Place one Checkpoint 2"
                    # self.ASR.unsubscribe("Test_ASR")
                    time.sleep(2)
                    # break

                if self.Word[1] >= 0.400 and self.Word[0] == '五号桌':
                    # self.Navigation.startLocalization()
                    print "Place one Checkpoint 1"
                    self.Motion.moveTo(0.25 * self.x + 0.5 * self.a, 0, 0)
                    self.Motion.moveTo(0, -1.5 * self.b - 2 * self.y - self.r, 0)
                    self.Motion.moveTo(0.5 * self.a + 0.25 * self.x, 0, 0)

                    # self.Motion.moveTo(0, 0, 0)
                    # self.Motion.moveTo(self.channel + self.d_Table, 0, 0)
                    # self.Motion.moveTo(0, 0, 3.14)
                    # self.Navigation.wait(Moving_Lab1, 1)

                    self.AnimSpeech.say("已到达五号桌，请说点餐来开启服务", self.configuration)
                    self.ASR.unsubscribe("Test_ASR")
                    self.Posture.goToPosture("StandInit", 0.5)
                    self.start = self.Word[0]
                    print "Place one Checkpoint 2"
                    # self.ASR.unsubscribe("Test_ASR")
                    time.sleep(2)
                    # break

                if self.Word[1] >= 0.400 and self.Word[0] == '六号桌':
                    # self.Navigation.startLocalization()
                    print "Place one Checkpoint 1"
                    self.Motion.moveTo(0.25 * self.x + 0.5 * self.a, 0, 0)
                    self.Motion.moveTo(0, -self.b - self.y, 0)
                    self.Motion.moveTo(0.5 * self.a + 0.25 * self.x, 0, 0)
                    # self.Navigation.wait(Moving_Lab1, 1)

                    self.AnimSpeech.say("已到达六号桌，请说点餐来开启服务", self.configuration)
                    self.ASR.unsubscribe("Test_ASR")
                    self.Posture.goToPosture("StandInit", 0.5)
                    self.start = self.Word[0]
                    print "Place one Checkpoint 2"
                    # self.ASR.unsubscribe("Test_ASR")
                    time.sleep(2)
                    # break

                if self.Word[1] >= 0.400 and self.Word[0] == '七号桌':
                    # self.Navigation.startLocalization()
                    print "Place one Checkpoint 1"
                    # self.Motion.moveTo(0, self.a, 0)
                    self.Motion.moveTo(0.25 * self.x + 0.5 * self.a, 0, 0)
                    self.Motion.moveTo(0, -1.5 * self.b - 2 * self.y - self.r, 0)
                    self.Motion.moveTo(0.5 * self.a + 0.75 * self.x, 0, 0)

                    # self.Navigation.wait(Moving_Lab1, 1)

                    self.AnimSpeech.say("已到达七号桌，请说点餐来开启服务", self.configuration)
                    self.ASR.unsubscribe("Test_ASR")
                    self.Posture.goToPosture("StandInit", 0.5)
                    self.start = self.Word[0]
                    print "Place one Checkpoint 2"
                    # self.ASR.unsubscribe("Test_ASR")
                    time.sleep(2)
                    # break

                if self.Word[1] >= 0.400 and self.Word[0] == '八号桌':
                    # self.Navigation.startLocalization()
                    print "Place one Checkpoint 1"
                    self.Motion.moveTo(0.25 * self.x + 0.5 * self.a, 0, 0)
                    self.Motion.moveTo(0, -self.b - self.y, 0)
                    self.Motion.moveTo(0.5 * self.a + 0.75 * self.x, 0, 0)
                    # self.Navigation.wait(Moving_Lab1, 1)

                    self.AnimSpeech.say("已到达八号桌，请说点餐来开启服务", self.configuration)
                    self.ASR.unsubscribe("Test_ASR")
                    self.Posture.goToPosture("StandInit", 0.5)
                    self.start = self.Word[0]
                    print "Place one Checkpoint 2"
                    # self.ASR.unsubscribe("Test_ASR")
                    time.sleep(2)
                    # break

                if self.Word[1] >= 0.400 and self.Word[0] == '九号桌':
                    # self.Navigation.startLocalization()
                    print "Place one Checkpoint 1"
                    self.Motion.moveTo(self.x + self.a, 0, 0)

                    # self.Navigation.wait(Moving_Lab1, 1)

                    self.AnimSpeech.say("已到达九号桌，请说点餐来开启服务", self.configuration)
                    self.ASR.unsubscribe("Test_ASR")
                    self.Posture.goToPosture("StandInit", 0.5)
                    self.start = self.Word[0]
                    print "Place one Checkpoint 2"
                    # self.ASR.unsubscribe("Test_ASR")
                    time.sleep(2)
                    # break

                if self.Word[1] >= 0.400 and self.Word[0] == '十号桌':
                    # self.Navigation.startLocalization()
                    print "Place one Checkpoint 1"

                    # self.Navigation.wait(Moving_Lab1, 1)

                    self.AnimSpeech.say("已到达十号桌，请说点餐来开启服务", self.configuration)
                    self.ASR.unsubscribe("Test_ASR")
                    self.Posture.goToPosture("StandInit", 0.5)
                    self.start = self.Word[0]
                    print "Place one Checkpoint 2"
                    # self.ASR.unsubscribe("Test_ASR")
                    time.sleep(2)
                    # break

    #  Home_Process方法功能是让一个机器人在听到不同的语音指令时做出相应的动作。
    def Home_Process(self):
        print "Thread1 started"

        while True:
            time.sleep(1)
            self.ASR.subscribe("Test_ASR")
            self.Word = self.Memory.getData("WordRecognized")
            data = self.Word[0].decode("utf-8")
            print("Word: ")
            print(data)
            print self.Word[1]
            data = data.encode("utf-8")

            if self.Word[1] >= 0.400 and data == '开始':
                print "Pepper recognized"
                self.Process2.start()
                self.start2 = self.start
                self.ASR.unsubscribe("Test_ASR")

            if self.Word[1] >= 0.400 and data == '点餐':
                print "Order recognized"
                self.Process5.start()
                time.sleep(5)
                self.Process5.join()
                self.ASR.unsubscribe("Test_ASR")

            if self.Word[1] >= 0.400 and data == '停止':
                self.Navigation.navigateToInMap(self.Navigation.getRobotPositionInMap()[0])
                self.ASR.unsubscribe("Test_ASR")
                print "Stoped"
                break

            if self.Word[1] >= 0.500 and data == '起点':
                self.Navigation.startLocalization()
                Moving_Lab = self.Navigation.navigateToInMap([0.0, 0.0, 0.0])
                self.Navigation.wait(Moving_Lab, 1)
                self.Navigation.stopLocalization()
                self.ASR.unsubscribe("Test_ASR")
                print "起点"
                break

    # Home_Process2 方法功能是让一个机器人在听到不同的语音指令时做出相应的动作。
    def Home_Process2(self):
        print "Thread3 started"

        while True:
            time.sleep(1)
            self.ASR.subscribe("Test_ASR")
            self.Word = self.Memory.getData("WordRecognized")
            data = self.Word[0].decode("utf-8")
            print("Word: ")
            print(data)
            print self.Word[1]
            data = data.encode("utf-8")

            if self.Word[1] >= 0.400 and data == '开始':
                print "Pepper recognized"
                # self.AnimSpeech.say("你好！pepper很高兴为你服务，请问前往几号桌?", self.configuration)

                self.Process4.start()
                self.ASR.unsubscribe("Test_ASR")

            if self.Word[1] >= 0.400 and data == '点餐':
                print "Order recognized"
                self.Process6.start()
                time.sleep(5)
                self.Process6.join()
                self.ASR.unsubscribe("Test_ASR")

            if self.Word[1] >= 0.400 and data == '停止':
                self.Navigation.navigateToInMap(self.Navigation.getRobotPositionInMap()[0])
                self.ASR.unsubscribe("Test_ASR")
                print "Stoped"

            if self.Word[1] >= 0.500 and data == '结束':
                self.ASR.unsubscribe("Test_ASR")
                print "点餐结束"

            if self.Word[1] >= 0.500 and data == '起点':
                if self.start == "一号桌":
                    self.Motion.moveTo(-0.25 * self.x - self.r, 0, 0)
                elif self.start == "三号桌":
                    self.Motion.moveTo(-0.75 * self.x - self.r, 0, 0)
                elif self.start == "二号桌":
                    self.Motion.moveTo(-0.25 * self.x - self.r, 0, 0)
                    self.Motion.moveTo(0, -0.5 * self.b - self.y - self.r, 0)
                elif self.start == "四号桌":
                    self.Motion.moveTo(-0.75 * self.x - self.r, 0, 0)
                    self.Motion.moveTo(0, -0.5 * self.b - self.y - self.r, 0)
                elif self.start == "五号桌":
                    self.Motion.moveTo(-1.25 * self.x - self.a - self.r, 0, 0)
                elif self.start == "七号桌":
                    self.Motion.moveTo(-1.75 * self.x - self.a - self.r, 0, 0)
                elif self.start == "六号桌":
                    self.Motion.moveTo(-0.25 * self.x - 0.5 * self.a, 0, 0)
                    self.Motion.moveTo(0, -0.5 * self.b - self.y - self.r, 0)
                    self.Motion.moveTo(-0.5 * self.a - self.x - self.r, 0, 0)
                elif self.start == "八号桌":
                    self.Motion.moveTo(-0.75 * self.x - 0.5 * self.a, 0, 0)
                    self.Motion.moveTo(0, -0.5 * self.b - self.y - self.r, 0)
                    self.Motion.moveTo(-0.5 * self.a - self.x - self.r, 0, 0)
                elif self.start == "九号桌":
                    self.Motion.moveTo(-1.75 * self.x - self.a - self.r, 0, 0)
                    self.Motion.moveTo(0, -1.5 * self.b - 2 * self.y - self.r, 0)
                elif self.start == "十号桌":
                    self.Motion.moveTo(-0.75 * self.x - self.a - self.r, 0, 0)
                    self.Motion.moveTo(0, -1.5 * self.b - 2 * self.y - self.r, 0)
                self.ASR.unsubscribe("Test_ASR")
                print "起点"
                break

    def Navig_In_Map(self):
        self.Process1 = threading.Thread(target=self.Home_Process)
        self.Process2 = threading.Thread(target=self.Navigation_Process)
        self.Process3 = threading.Thread(target=self.Home_Process2)
        self.Process4 = threading.Thread(target=self.Navigation_Process2)
        self.Process5 = threading.Thread(target=self.order_Process)
        self.Process6 = threading.Thread(target=self.order_Process)
        # self.Thread1.daemon = True

        self.Process1.start()
        time.sleep(5)
        self.Process1.join()

        self.Process3.start()
        time.sleep(5)
        self.Process3.join()

        print "Completed"


if __name__ == '__main__':
    navig = Navig()
    navig.Config_Navig()
    navig.Navig_In_Map()
    # print navig.ASR.getAvailableLanguages()

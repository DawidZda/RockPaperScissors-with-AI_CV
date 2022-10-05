import random
import cvzone
import cv2
from cvzone.HandTrackingModule import HandDetector
import time


cap = cv2.VideoCapture(0)

# Setting cap to work on all cameras
cap.set(3, 640)
cap.set(4, 480)

timer = 0
stateResult = False
startGame = False
scores = [0, 0] # [AI, Player]

detector = HandDetector(maxHands=1)

while True:
    imgBackground = cv2.imread("Resources/Background.png")
    success, img = cap.read()


    # Setting width
    # No specific img number, output None, 480 ( cap.set ) / 600 ( image background ) = 0.8 + 0.25 (to fit well)
    imgScaled = cv2.resize(img, (0, 0), None, 0.825, 0.825)



    # Setting display
    imgScaled = imgScaled[:, 105:375]

    # Find hands
    hands, img = detector.findHands(imgScaled)  # with draw
    if startGame:

        if stateResult is False:
            timer = time.time() - initialTime
            # Scale = 3, green(20) blue(65) red(220), thickness = 2
            cv2.putText(imgBackground, str(int(timer)), (370, 360),  cv2.FONT_HERSHEY_DUPLEX, 3, (20, 65, 220), 2)

            # Set timer count to 3
            if timer > 3:
                stateResult = True
                timer = 0

        # Get fingersUp from hand
                if hands:
                    playerHand = None
                    hand = hands[0]
                    fingers = detector.fingersUp(hand)
                    if fingers == [0, 0, 0, 0, 0]:
                        playerHand = 1
                    if fingers == [1, 1, 1, 1, 1]:
                        playerHand = 2
                    if fingers == [0, 1, 1, 0, 0]:
                        playerHand = 3
                    #print(playerHand)

                    # Setting AI / dynamic typing
                    randomNumber = random.randint(1, 3)
                    imgAI = cv2.imread(f'Resources/{randomNumber}.png', cv2.IMREAD_UNCHANGED)
                    imgAIResized = cv2.resize(imgAI, (290, 290), None, 0.825, 0.825)
                    imgAIResized = imgAIResized[:, 0:350]


                    # AI Wins
                    if (playerHand == 3 and randomNumber == 1) or \
                        (playerHand == 1 and randomNumber == 2) or \
                        (playerHand == 2 and randomNumber == 3):
                        scores[0] += 1


                    # Player Wins
                    if (playerHand == 1 and randomNumber == 3) or \
                        (playerHand == 2 and randomNumber == 1) or \
                        (playerHand == 3 and randomNumber == 2):
                        scores[1] += 1

    # Setting camera for player

    imgBackground[144:540, 496:766] = imgScaled
    if stateResult:
          imgBackground = cvzone.overlayPNG(imgBackground, imgAIResized, (20, 200))

    cv2.putText(imgBackground, str((scores[0])), (45, 135), cv2.FONT_HERSHEY_PLAIN, 3, (0, 0, 0), 3)
    cv2.putText(imgBackground, str((scores[1])), (725, 135), cv2.FONT_HERSHEY_PLAIN, 3, (0, 0, 0), 3)
    cv2.imshow("Background", imgBackground)
    key = cv2.waitKey(1)

    # Press Enter to start game
    if key == ord("\r"):
        startGame = True
        initialTime = time.time()
        stateResult = False





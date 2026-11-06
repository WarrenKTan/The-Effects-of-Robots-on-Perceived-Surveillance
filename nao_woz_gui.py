import tkinter as tk # python interactable panel library
import qi # nao API
import math # joint movement
from PIL import Image, ImageTk # rendering images in tkinter
import threading # threading image retrieval from camera
import sys, signal # closing application


# NAO services. loaded in connectNao
session = None
tts_service = None
motion_service = None
posture_service = None
audio_service = None

# NAO video
video_service = None
cameraID = None
cameraLabel = None

# threading
latestFrame = None
frameLock = threading.Lock()
cameraStop = threading.Event()
cameraThread = None

# main window with three panels
root = tk.Tk()
root.title("NAO HRI Control Panel")
root.geometry("700x600")

root.rowconfigure(2, weight=2)

# column grid (1)
root.columnconfigure(0, weight=1)

# make the main panels
panel1 = tk.Frame(
            root,
            # bg="red",
            highlightthickness=4,
            bd=2,
            relief="solid"
        )
panel2 = tk.Frame(
            root,
            # bg="green",
            highlightthickness=4,
            bd=2,
            relief="solid"
        )
panel3 = tk.Frame(
            root,
            # bg="blue",
            highlightthickness=4,
            bd=2,
            relief="solid"
        )

# Put each panel in its own row
panel1.grid(
    row=0,
    column=0,
    sticky="nsew"
)
panel2.grid(
    row=1,
    column=0,
    sticky="nsew"
)
panel3.grid(
    row=2,
    column=0,
    sticky="nsew"
)

# connect to Nao
def connectNao(naoIP):
    # global variables
    global session
    global tts_service
    global motion_service
    global posture_service
    global audio_service
    global video_service
    global cameraID

    try:
        session = qi.Session()
        print(f"Connecting to NAO at {naoIP}:9559...")
        session.connect(f"tcp://{naoIP}:9559")
        print("Successfully connected to NAO!")
    except RuntimeError as e:
        print(f"Failed to connect to the robot at {naoIP}: {e}")
        return False
    except:
        print(f"Failed to start qi session")
        return False

    try:
        print("Initialising NAO services...")
        tts_service = session.service("ALTextToSpeech")
        motion_service  = session.service("ALMotion")
        posture_service = session.service("ALRobotPosture")
        audio_service = session.service("ALAudioDevice")
        video_service = session.service("ALVideoDevice")
        print("NAO services successfully initialised!")
    except Exception as e:
        print(f"Failed to load services: {e}")
        return False

    # setup camera
    # Name: NAO_WOZ_Camera
    # Camera: Top (forehead) Camera
    # Resolution: 320x240px
    # Colour Space: RGB
    # Frames per Second: 15fps
    print("Setting up NAO camera...")
    cameraID = video_service.subscribeCamera("NAO_WOZ_Camera", 0, 1, 11, 15)
    print("NAO camera successfully setup!")

    # executed properly
    audio_service.setOutputVolume(60)
    tts_service.say("Connected to Nao")
    posture_service.goToPosture("Sit", 0.1)
    motion_service.setAngles("HeadPitch", math.radians(10), 0.1)

    return True

# connection to Nao
def fillPanel1(panel = panel1):
    # create horizontally aligned frame
    frame = tk.Frame(panel)
    frame.pack(anchor="w", padx=5, pady=5)

    # prompt user
    textBox = tk.Label(frame, text="Enter the Robot's IP:")
    
    # text input 
    textInput = tk.Entry(frame)

    # status label
    statusLabel = tk.Label(
        frame,
        text="Status: Not Connected",
        fg="red"
    )
    statusLabel.pack(side="right", padx=5)

    # function called when button is clicked
    def submit():
        naoIP = textInput.get()

        # start connecting to NAO
        connected = connectNao(naoIP)

        if connected:
            print("Connection successful")
            statusLabel.config(
                text=f"Status: Connected at {naoIP}",
                fg="green"
            )

            startCamera()
        else:
            statusLabel.config(
                text=f"Status: Not Connected",
                fg="red"
            )
            print("Connection failed")

    # submit button
    submitButton = tk.Button(
        frame,
        text="Connect",
        bg="green",
        # replace with connection function
        command=submit
    )

    objects = [textBox, textInput, submitButton]

    # pack all
    for _, object in enumerate(objects):
        object.pack(
            side="left",
            padx=5
        )

# robot head movement and actions
def fillPanel2(panel = panel2):
    # create sections
    section1 = tk.Frame(panel, bd=1, relief="flat")
    section2 = tk.Frame(panel, bd=1, relief="flat")
    section3 = tk.Frame(panel, bd=1, relief="flat")

    # pack sections
    sections = [section1, section2, section3]
    for _, object in enumerate(sections):
        object.pack(
            side="left",
            fill="both",
            expand=True
        )

    # create and pack buttons
    button1_1 = tk.Button(section1, text="Look Left", command=lambda: headLook(20))
    for button in [button1_1]:
        button.pack(fill="x", padx=5, pady=5)

    button2_1 = tk.Button(section2, text="Look Middle", command=lambda: headLook(0))
    for button in [button2_1]:
        button.pack(fill="x", padx=5, pady=5)

    button3_1 = tk.Button(section3, text="Look Right", command=lambda: headLook(-20))
    for button in [button3_1]:
        button.pack(fill="x", padx=5, pady=5)

# turn NAO head yaw to 'angle' degrees
def headLook(angle = 0):
    try: 
        motion_service.setAngles("HeadYaw", math.radians(angle), 0.1)
    except AttributeError:
        print("The NAO motion service is not available. Try reconnecting the NAO robot to the application and try again.")

# camera communication
def fillPanel3(panel = panel3):
    global cameraLabel

    # horizontally aligned frame
    frame0 = tk.Frame(panel)
    frame0.pack(anchor="w", padx=5, pady=5)

    # Robot Camera Feed label
    textBox1 = tk.Label(frame0, text="Robot Camera Feed")
    textBox1.pack(
        side="left",
        padx=5
    )

    # Robot Camera Feed
    cameraLabel = tk.Label(panel)
    cameraLabel.pack(
        anchor="center",
        padx=5,
        pady=5
    )

# update the camera to most recent frame
def updateCamera():

    with frameLock:
        frame = latestFrame

    if frame is not None:
        width, height, image_bytes = frame

        image = Image.frombytes(
            "RGB",
            (width, height),
            image_bytes
        )

        photo = ImageTk.PhotoImage(image)

        cameraLabel.config(image=photo)
        cameraLabel.image = photo

    root.after(66, updateCamera)
    
def cameraWorker():
    global latestFrame

    while not cameraStop.is_set():
        image_data = None

        try:
            image_data = video_service.getImageRemote(cameraID)

            if image_data:
                width = image_data[0]
                height = image_data[1]
                image_bytes = bytes(image_data[6])

                # Store only the newest frame
                with frameLock:
                    latestFrame = (width, height, image_bytes)

        except Exception as e:
            print(f"Camera retrieval error: {e}")
            break

        finally:
            if image_data:
                try:
                    video_service.releaseImage(cameraID)
                except Exception as e:
                    print(f"Image release error: {e}")

def startCamera():
    global cameraThread

    if cameraThread is not None and cameraThread.is_alive():
        return

    cameraStop.clear()

    cameraThread = threading.Thread(
        target=cameraWorker,
        daemon=True
    )

    cameraThread.start()

    # Start Tkinter rendering
    updateCamera()

def closeApplication():
    global cameraID

    print("Closing application...")

    cameraStop.set()

    if cameraThread is not None:
        cameraThread.join(timeout=2)

    try:
        if video_service is not None and cameraID is not None:
            video_service.unsubscribe(cameraID)
            cameraID = None

        if session is not None:
            session.close()

    except Exception as e:
        print(f"Cleanup error: {e}")

    root.destroy()

# run camera threading cleaner upon application close
root.protocol("WM_DELETE_WINDOW", closeApplication)

fillPanel1(panel1)
fillPanel2(panel2)
fillPanel3(panel3)

root.mainloop()
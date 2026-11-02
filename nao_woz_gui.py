import tkinter as tk
import qi, math


# services. loaded in connectNao
session = None
tts_service = None
motion_service = None
posture_service = None
audio_service = None
leds_service = None

# main window with three panels
# region
root = tk.Tk()
root.title("NAO HRI Control Panel")
root.geometry("700x400")

# row grid (3)
for i in range(3):
    root.rowconfigure(i, weight=1)

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
# endregion

# connect to Nao
def connectNao(naoIP):
    # global variables
    global session
    global tts_service
    global motion_service
    global posture_service
    global audio_service
    global leds_service

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
        tts_service = session.service("ALTextToSpeech")
        motion_service  = session.service("ALMotion")
        posture_service = session.service("ALRobotPosture")
        audio_service = session.service("ALAudioDevice")
        leds_service = session.service("ALLeds")
    except Exception as e:
        print(f"Failed to load services: {e}")
        return False

    # executed properly
    audio_service.setOutputVolume(60)
    leds_service.fadeRGB("FaceLeds", 0x0000FF, 0.5)
    tts_service.say("Connected to Nao")
    posture_service.goToPosture("Sit", 0.5)
    return True

# connection to Nao
def fillPanel1(panel = panel1):
    # horizontally aligned frame
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

    # Function called when button is clicked
    def submit():
        naoIP = textInput.get()

        connected = connectNao(naoIP)

        if connected:
            print("Connection successful")
            statusLabel.config(
                text=f"Status: Connected at {naoIP}",
                fg="green"
            )
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

# built-in and/or custom speech
def fillPanel2(panel = panel2):
    # horizontally aligned frame
    frame0 = tk.Frame(panel)
    frame0.pack(anchor="w", padx=5, pady=5)

    # Built-in Speech label
    textBox1 = tk.Label(frame0, text="Built-in Speech")
    textBox1.pack(
        side="left",
        padx=5
    )

    # horizontally aligned frame
    frame1 = tk.Frame(panel)
    frame1.pack(anchor="w", padx=5, pady=5)

    greetButton = tk.Button(
        frame1,
        text="Greeting",
        # replace with function
        command=lambda: tts_service.say(f"Hello! My name is Nao!")
    )

    instructionButton = tk.Button(
        frame1,
        text="Instructions",
        # replace with function
        command=lambda: tts_service.say(f"To perform the Three Good Things exercise, we can discuss three good things from your day. Let's try it out!")
    )

    exampleButton = tk.Button(
        frame1,
        text="Example",
        # replace with function
        command=lambda: tts_service.say(f"I'll start first. Today, I was fully charged, had my motors cleaned, and got to chat with my creators. Now you try.")
    )

    farewellButton = tk.Button(
        frame1,
        text="Farewell",
        # replace with function
        command=lambda: tts_service.say(f"Thank you for your participation. Have a good day!")
    )

    frame1_objects = [greetButton, instructionButton, exampleButton, farewellButton]

    # pack objects in frame1
    for _, object in enumerate(frame1_objects):
        object.pack(
            side="left",
            padx=5
        )

    # horizontally aligned frame2
    frame2 = tk.Frame(panel)
    frame2.pack(anchor="w", padx=5, pady=5)

    # prompt user
    textBox2 = tk.Label(frame2, text="Custom Speech Entry")
    
    # text input
    textInput = tk.Entry(frame2)

    # submit button
    submitButton = tk.Button(
        frame2,
        text="Send Speech",
        bg="#2196f3",
        # replace with connection function
        command=lambda: tts_service.say(f"{textInput.get()}")
    )

    objects = [textBox2, textInput, submitButton]

    # pack all
    for _, object in enumerate(objects):
        object.pack(
            side="left",
            expand=True,
            padx=5
        )

# robot movement, LEDs, or actions
def fillPanel3(panel = panel3):
    # create sections
    # region
    section1 = tk.Frame(panel, bd=1, relief="solid")
    section2 = tk.Frame(panel, bd=1, relief="solid")
    section3 = tk.Frame(panel, bd=1, relief="solid")

    # pack sections
    sections = [section1, section2, section3]
    for _, object in enumerate(sections):
        object.pack(
            side="left",
            fill="both",
            expand=True
        )

    # endregion

    # create and pack section 1 buttons
    # region
    def nodHead():
        motion_service.setAngles("HeadPitch", math.radians(15), 0.1)
        motion_service.setAngles("HeadPitch", math.radians(0), 0.1)

    button1_1 = tk.Button(section1, text="Nod Head", command=nodHead)

    for button in [button1_1]:
        button.pack(fill="x", padx=5, pady=5)

    # endregion
    
    # create and pack section 2 buttons
    # region
    button2_1 = tk.Button(section2, text="Blue", bg="#30c7c2", command=lambda: leds_service.fadeRGB("FaceLeds", 0x0000FF, 0.5))
    button2_2 = tk.Button(section2, text="Green", bg="#30c73c", command=lambda: leds_service.fadeRGB("FaceLeds", 0x00FF00, 0.5))
    button2_3 = tk.Button(section2, text="Red", bg="#bf342a", command=lambda: leds_service.fadeRGB("FaceLeds", 0xFF0000, 0.5))

    for button in [button2_1, button2_2, button2_3]:
        button.pack(fill="x", padx=5, pady=5)

    # endregion

    # create and pack section 3 buttons
    # region
    button3_1 = tk.Button(section3, text="Sit", command=lambda: posture_service.goToPosture("Sit", 0.5))
    button3_2 = tk.Button(section3, text="Stand", command=lambda: posture_service.goToPosture("Stand", 0.5))

    for button in [button3_1, button3_2]:
        button.pack(fill="x", padx=5, pady=5)

    # endregion

fillPanel1(panel1)
fillPanel2(panel2)
fillPanel3(panel3)

root.mainloop()
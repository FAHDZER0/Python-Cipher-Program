from pathlib import Path
import string
import subprocess
import sys
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage, filedialog, messagebox
import encryption_utils
import decryption_utils

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"C:\Users\HP\Desktop\Let's hope it works\PY-progects\Tkinter-Designer-master\2\build\assets\frame1")

# Check if at least one argument (cipher_type) is provided
if len(sys.argv) > 1:
    # Access the cipher_type passed as the first argument (index 1)
    cipher_type = sys.argv[1]
    print("Received cipher_type:", cipher_type)
else:
    cipher_type = "error"
    print("No cipher_type provided.")
    subprocess.Popen(["python", "C:\\Users\\HP\\Desktop\\Let's hope it works\\PY-progects\\Tkinter-Designer-master\\2\\build\\gui.py"])
    window.destroy() # type: ignore


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

def open_Main_window():
    # Close the current window
    window.destroy()
    
    # Run the other script named gui.py
    subprocess.Popen(["python", "C:\\Users\\HP\\Desktop\\Let's hope it works\\PY-progects\\Tkinter-Designer-master\\2\\build\\gui.py"])

def Encryption_button_click():
    PlainText = get_PlainText()
    Key = get_Key(Encryption_Key_Text_Box) 
    a, b = get_A_And_B(Encryption_Key_Text_Box)
    if PlainText and (Key or (a and b)):
        if cipher_type == "Shift / Root 13":                                                #Shift Done
            encrypted_message = encryption_utils.shift_cipher_encrypt(PlainText, Key)  
        elif cipher_type == "AES":                                                          #AES Done
            encrypted_message = encryption_utils.AES_Encryption(PlainText, Key)  
        elif cipher_type == "Play Fair":                                                    #playfair Done
            encrypted_message = encryption_utils.Play_Fair_Encryption(PlainText, Key)  
        elif cipher_type == "Substitution":                                                 #Substitution Done
            encrypted_message = encryption_utils.Substitution_encrypt(PlainText, Key)  
        elif cipher_type == "Rail Fence":                                                   #Rail Fence Done
            encrypted_message = encryption_utils.rail_fence_encrypt(PlainText, Key)  
        elif cipher_type == "Row-Column":                                                   #Row Column Done
            encrypted_message = encryption_utils.row_column_encrypt(PlainText, Key)  
        elif cipher_type == "Vigenere":                                                     #Vigenere Done
            encrypted_message = encryption_utils.vigenere_encrypt(PlainText, Key)  
        elif cipher_type == "Affine":                                                       #Affine Done
            encrypted_message = encryption_utils.affine_encrypt(PlainText, a , b)   
        elif cipher_type == "RSA":                                                        #RSA Done
            encrypted_message = encryption_utils.enc_rsa_algo(PlainText, a , b)   
        elif cipher_type == "Hill":                                                         #Hill Done
            encrypted_message = encryption_utils.Hill_Cipher_encrypt(PlainText, Key)  
        elif cipher_type == "DES":                                                          #DES Done
            encrypted_message = encryption_utils.Des_Encryption(PlainText, Key)             
        else:
            print("Error in selecting encryption algorithm")
        print("Encrypted message:", encrypted_message)
        set_Encrypted_Message(encrypted_message)
        
    else:
        print("Error in plaintext or key.")

def get_PlainText():
    """
    Function to get the plaintext from a text widget and return it as a string.
    Display error message in a pop-up window and print in the console if the input is empty.
    """
    plaintext = Messge_to_Encrypt_Text_Area.get("1.0", "end-1c")  # Get the plaintext as a string
    if not plaintext.strip():  # Check if the plaintext is empty or contains only whitespace
        error_message = "Please enter some text."
        print(error_message)  # Print error message in the console
        messagebox.showerror("Error", error_message)  # Show error message in a pop-up window
        return None
    elif not ''.join(c for c in plaintext if c not in (' ', '\n', '\r')).isalpha():  # Check if the plaintext contains non-alphabetic characters (excluding spaces and end-of-line characters)
        error_message = "Please enter only alphabetic characters (excluding spaces and end-of-line characters)."
        print(error_message)  # Print error message in the console
        messagebox.showerror("Error", error_message)  # Show error message in a pop-up window
        return None
    else:
        return plaintext

def set_Encrypted_Message(encrypted_message):
    Encrypted_Message_Text_Area.delete("1.0", "end")
    Encrypted_Message_Text_Area.insert("1.0", encrypted_message)

def get_Key(Key_Text_Box):
    key_str = Key_Text_Box.get()  # Get the key value as a string
    try:
        if cipher_type == "Shift / Root 13" :
            key = int(key_str)  # For Cipher, key is an integer
        elif cipher_type == "Rail Fence":
            key_str = int(key_str) 
            if key_str <= 1 :
                messagebox.showerror("Error", "Key should be higher than 1")
            else:
                key = int(key_str)  # For Cipher, key is an integer
        elif cipher_type == "Play Fair" or cipher_type == "Row-Column" or cipher_type == "AES" or cipher_type == "Hill":
            if not key_str.strip():
                messagebox.showerror("Error", "Key should not be empty.")
            elif any(char.isdigit() for char in key_str):
                messagebox.showerror("Error", "Key should not contain numbers.")
            else:
                key = key_str
        elif cipher_type == "Substitution":
            if set(key_str.lower()) != set(string.ascii_lowercase) or len(key_str) != 26:
                messagebox.showerror("Error","Key must contain all alphabets.")
            else:
                key = key_str
        elif cipher_type == "Vigenere":
            if not key_str.isalpha():
                messagebox.showerror("Error", "Key must be alphabetic only")
                return None
            else:
                key = key_str
        elif cipher_type == "DES":
            key = key_str
        elif cipher_type == "Affine" or cipher_type == "RSA":
            Lhalf=""
            Rhalf=""
            i=0
            key_str = key_str.replace(" ","")
            for c in key_str:
                if c == ',':break
                i+=1
            Lhalf=key_str[0:i]
            Rhalf=key_str[i+1:]
            flag=False
            print(key_str)
            if any((not char.isdigit())  for char in Lhalf) or any((not char.isdigit())  for char in Rhalf) or len(Lhalf) == 0 or len(Rhalf) == 0 :
                messagebox.showerror("Error","Enter a and b seperated by comma")
            else:
                key = key_str
        else:
            raise ValueError("Unsupported cipher type.")
        return key
    except ValueError:
        error_message = "Invalid key value."
        print(error_message)  # Print error message in the console
        messagebox.showerror("Error", error_message)  # Show error message in a pop-up window

def get_A_And_B(Key_Text_Box):
    key_str = Key_Text_Box.get()  # Get the key value as a string
    # Split the text by comma and space
    numbers = key_str.split(',')
    
    # If there are not exactly two numbers, return None
    if len(numbers) != 2:
        return None, None
    
    # Extract and convert the numbers to integers
    num1 = int(numbers[0])
    num2 = int(numbers[1])
    
    return num1, num2

def get_Encrypted_message():
    """
    Function to get the plaintext from a text widget and return it as a string.
    Display error message in a pop-up window and print in the console if the input is empty.
    """
    encrypted_message = Encrypted_Message_Text_Area.get("1.0", "end-1c")  # Get the plaintext as a string
    if not encrypted_message.strip():  # Check if the plaintext is empty or contains only whitespace
        error_message = "There is No Encrypted Text to Download."
        print(error_message)  # Print error message in the console
        messagebox.showerror("Error", error_message)  # Show error message in a pop-up window
    else:
        return encrypted_message

# ----------------------------------------------------------------

def get_Text_To_Decrypt():
    """
    Function to get the Encrypted_Text from a text widget and return it as a string.
    Display error message in a pop-up window and print in the console if the input is empty.
    """
    Encrypted_Text = Messge_to_Decrypt_Text_Area.get("1.0", "end-1c")  # Get the Encrypted Text as a string
    if not Encrypted_Text.strip():  # Check if the Encrypted Text is empty or contains only whitespace
        error_message = "Please enter some text."
        print(error_message)  # Print error message in the console
        messagebox.showerror("Error", error_message)  # Show error message in a pop-up window
    elif not ''.join(c for c in Encrypted_Text if c not in (' ', '\n', '\r')).isalpha():  # Check if the plaintext contains non-alphabetic characters (excluding spaces and end-of-line characters)
        error_message = "Please enter only alphabetic characters (excluding spaces and end-of-line characters)."
        print(error_message)  # Print error message in the console
        messagebox.showerror("Error", error_message)  # Show error message in a pop-up window
        return None
    else:
        return Encrypted_Text

def get_Decrypted_message():
    """
    Function to get the plaintext from a text widget and return it as a string.
    Display error message in a pop-up window and print in the console if the input is empty.
    """
    decrypted_message = Decrypted_Message_Text_Area.get("1.0", "end-1c")  # Get the plaintext as a string
    if not decrypted_message.strip():  # Check if the plaintext is empty or contains only whitespace
        error_message = "There is No Decrypted Text to Download."
        print(error_message)  # Print error message in the console
        messagebox.showerror("Error", error_message)  # Show error message in a pop-up window
    else:
        return decrypted_message

def set_Decrypted_Message(decrypted_message):
    Decrypted_Message_Text_Area.delete("1.0", "end")
    Decrypted_Message_Text_Area.insert("1.0", decrypted_message)

def Decryption_button_click():
    Cipher_Text = get_Text_To_Decrypt()
    Key = get_Key(Decryption_Key_Text_Box) 
    a, b = get_A_And_B(Decryption_Key_Text_Box)    
    if Cipher_Text and (Key or (a and b)):
        if cipher_type == "Shift / Root 13":                                                #Shift Done
            decrypted_message = decryption_utils.shift_cipher_decrypt(Cipher_Text, Key)  
        elif cipher_type == "AES":                                                          #AES Done
            decrypted_message = decryption_utils.AES_Decryption(Cipher_Text, Key)  
        elif cipher_type == "Play Fair":                                                    #playfair Done
            decrypted_message = decryption_utils.Play_Fair_Decryption(Cipher_Text, Key)  
        elif cipher_type == "Substitution":                                                 #Substitution Done
            decrypted_message = decryption_utils.Substitution_decrypt(Cipher_Text, Key)  
        elif cipher_type == "Rail Fence":                                                   #Rail Fence Done
            decrypted_message = decryption_utils.rail_fence_decrypt(Cipher_Text, Key)  
        elif cipher_type == "Row-Column":                                                   #Row Column Done
            decrypted_message = decryption_utils.row_column_decrypt(Cipher_Text, Key)  
        elif cipher_type == "Vigenere":                                                     #Vigenere Done
            decrypted_message = decryption_utils.vigenere_decrypt(Cipher_Text, Key)  
        elif cipher_type == "Affine":                                                       #Affine Done
            decrypted_message = decryption_utils.affine_decrypt(Cipher_Text, a , b)   
        elif cipher_type == "Hill":                                                         #Hill Done
            decrypted_message = decryption_utils.Hill_Cipher_decrypt(Cipher_Text, Key)  
        elif cipher_type == "RSA":                                                          #RSA Done
            decrypted_message = decryption_utils.dec_rsa_algo(Cipher_Text, a , b)
        elif cipher_type == "DES":                                                          #DES Done
            decrypted_message = decryption_utils.Des_Decryption(Cipher_Text, Key)             
        else:
            print("Error in selecting decryption algorithm")
        print("Decrypted message:", decrypted_message)
        set_Decrypted_Message(decrypted_message)
        
    else:
        print("Error in Encrypted or key.")

def download(type):
    if type == "Encrypted":
        message = get_Encrypted_message()
    else:
        message = get_Decrypted_message()
    if message is not None:
        file_path = filedialog.asksaveasfilename(defaultextension=".txt",filetypes=[("Text files", "*.txt")],title=f"Save {type} Message As")
        
        if file_path:
            # Write the encrypted message to the chosen file
            with open(file_path, "w") as file:
                file.write(message)
            
            messagebox.showinfo("Download", "Your Encrypted Message is Downloaded Successfully.")
        else:
            messagebox.showinfo("Download", "Download Cancelled.")

def add_content(type):
    # Ask the user to choose the file
    
    file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")],title="Choose File")
    
    if file_path:
        # Open the selected file and read its content
        with open(file_path, "r") as file:
            file_content = file.read()
        
        # Insert the file content into the entry widget
        if type == "Encrypted":
            Messge_to_Encrypt_Text_Area.delete("1.0", "end")
            Messge_to_Encrypt_Text_Area.insert("1.0", file_content)
        else:
            Messge_to_Decrypt_Text_Area.delete("1.0", "end")
            Messge_to_Decrypt_Text_Area.insert("1.0", file_content)

        
        messagebox.showinfo("File Loaded", "Content from the selected file has been loaded.")
    else:
        messagebox.showinfo("No File Selected", "No file selected. Operation cancelled.")

def center_window(window, width, height):
    """
    Function to center a window on the screen.
    """
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    x = (screen_width - width) // 2
    y = (screen_height - height) // 2

    window.geometry(f"{width}x{height}+{x}+{y}")

if cipher_type == "Shift / Root 13":
    messagebox.showinfo("Shift / Root 13", "By Default the Key is set to 13 for Root 13.")
elif cipher_type == "Affine":
    messagebox.showinfo("Affine Cipher", 'Separate the "a" and "b" By ONLY ",".')
elif cipher_type == "Substitution":
    messagebox.showinfo("Substitution Cipher", 'Enter All The Alphabet in the order you want in the Key.')


window = Tk()
window.geometry("977x785")
window.configure(bg = "#363434")
window.title("Cryptography")
center_window(window, 977, 785)

#---------------------Main Window------------------------
canvas = Canvas(
    window,
    bg = "#363434",
    height = 785,
    width = 977,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)

canvas.place(x = 0, y = 0)
image_image_1 = PhotoImage(
    file=relative_to_assets("image_1.png"))
image_1 = canvas.create_image(
    488.0,
    30.0,
    image=image_image_1
)

#---------------------Title-----------------------------

canvas.create_text(
    59.0,
    18.0,
    anchor="nw",
    text= cipher_type + " Cipher",
    fill="#000000",
    font=("Inter Bold", 24 * -1)
)

#----------Messge to Encrypt Text Area-------------------
entry_image_1 = PhotoImage(
    file=relative_to_assets("Messge_to_Encrypt_Text_Area.png"))
entry_bg_1 = canvas.create_image(
    205.5,
    218.5,
    image=entry_image_1
)
Messge_to_Encrypt_Text_Area = Text(
    bd=0,
    bg="#D9D9D9",
    fg="#000716",
    font=("Inter Semibold", 20 * -1),
    highlightthickness=0
)
Messge_to_Encrypt_Text_Area.place(
    x=49.0,
    y=129.0,
    width=313.0,
    height=177.0
)

#--------------Encrypted Message Text Area---------------
entry_image_2 = PhotoImage(
    file=relative_to_assets("Encrypted_Message_Text_Area.png"))
entry_bg_2 = canvas.create_image(
    205.5,
    596.5,
    image=entry_image_2
)
Encrypted_Message_Text_Area = Text(
    bd=0,
    bg="#D9D9D9",
    fg="#000716",
    font=("Inter Semibold", 20 * -1),
    highlightthickness=0
)
Encrypted_Message_Text_Area.place(
    x=49.0,
    y=507.0,
    width=313.0,
    height=177.0
)

#--------------Decrypted Message Text Area---------------
entry_image_3 = PhotoImage(
    file=relative_to_assets("Decrypted_Message_Text_Area.png"))
entry_bg_3 = canvas.create_image(
    752.5,
    596.5,
    image=entry_image_3
)
Decrypted_Message_Text_Area = Text(
    bd=0,
    bg="#D9D9D9",
    fg="#000716",
    font=("Inter Semibold", 20 * -1),
    highlightthickness=0
)
Decrypted_Message_Text_Area.place(
    x=596.0,
    y=507.0,
    width=313.0,
    height=177.0
)

#----------Messge to Decrypt Text Area-------------------
entry_image_4 = PhotoImage(
    file=relative_to_assets("Messge_to_Decrypt_Text_Area.png"))
entry_bg_4 = canvas.create_image(
    752.5,
    218.5,
    image=entry_image_4
)
Messge_to_Decrypt_Text_Area = Text(
    bd=0,
    bg="#D9D9D9",
    fg="#000716",
    font=("Inter Semibold", 20 * -1),
    highlightthickness=0
)
Messge_to_Decrypt_Text_Area.place(
    x=596.0,
    y=129.0,
    width=313.0,
    height=177.0
)

#-------------------Messge to Encrypt---------------------
canvas.create_text(
    102.0,
    92.0,
    anchor="nw",
    text="Message to Encrypt",
    fill="#F3EFE7",
    font=("Inter Bold", 16 * -1)
)

#-------------------Messge to Decrypt---------------------
canvas.create_text(
    649.0,
    98.0,
    anchor="nw",
    text="Message to Decrypt",
    fill="#F3EFE7",
    font=("Inter Bold", 16 * -1)
)

#---------------------Encryption Key-----------------------
canvas.create_text(
        21.0,
        354.0,
        anchor="nw",
        text="Encryption Key",
        fill="#FFFFFF",
        font=("Inter Bold", 16 * -1)
    )

#---------------------Decryption Key-----------------------
canvas.create_text(
        570.0,
        351.0,
        anchor="nw",
        text="Decryption Key",
        fill="#D6D6CC",
        font=("Inter Bold", 16 * -1)
    )

#---------------Encryption Key Text Box--------------------
entry_image_5 = PhotoImage(
    file=relative_to_assets("Encryption_Key_Text_Box.png"))
entry_bg_5 = canvas.create_image(
    273.0,
    365.5,
    image=entry_image_5
)
Encryption_Key_Text_Box = Entry(
    bd=0,
    bg="#D9D9D9",
    fg="#000716",
    font=("Inter Semibold", 20 * -1),
    highlightthickness=0
)
Encryption_Key_Text_Box.place(
    x=181.0,
    y=351.0,
    width=184.0,
    height=27.0
)
if cipher_type == "Shift / Root 13":
    Encryption_Key_Text_Box.insert(0, "13")

#---------------Decryption Key Text Box--------------------
entry_image_6 = PhotoImage(
    file=relative_to_assets("Decryption_Key_Text_Box.png"))
entry_bg_6 = canvas.create_image(
    820.0,
    357.5,
    image=entry_image_6
)
Decryption_Key_Text_Box = Entry(
    bd=0,
    bg="#D9D9D9",
    fg="#000716",
    font=("Inter Semibold", 20 * -1),
    highlightthickness=0
)
Decryption_Key_Text_Box.place(
    x=728.0,
    y=343.0,
    width=184.0,
    height=27.0
)
if cipher_type == "Shift / Root 13":
    Decryption_Key_Text_Box.insert(0, "13")

#------------------Encryption Button-----------------------
button_image_1 = PhotoImage(
    file=relative_to_assets("Encryption_Button.png"))
Encryption_Button = Button(
    background="#363434",
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=Encryption_button_click,  # Call button_click function when clicked
    relief="flat"
)
Encryption_Button.place(
    x=34.0,
    y=429.0,
    width=121.0,
    height=39.0
)

#------------------Upload Encryption Button-------------------
button_image_2 = PhotoImage(
    file=relative_to_assets("Upload_Encryption_Button.png"))
Upload_Encryption_Button = Button(
    background="#363434",
    image=button_image_2,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: add_content("Encrypted"),
    relief="flat"
)
Upload_Encryption_Button.place(
    x=209.0,
    y=428.0,
    width=40.0,
    height=40.0
)

#------------------Downlaod Encryption Button-------------------
button_image_6 = PhotoImage(
    file=relative_to_assets("image_download.png"))
Downlaod_Encryption_Button = Button(
    background="#363434",
    image=button_image_6,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: download("Encrypted"),
    relief="flat"
)
Downlaod_Encryption_Button.place(
    x=264.0,
    y=428.0,
    width=40.0,
    height=40.0
)

#------------------Decryption Button-----------------------
button_image_3 = PhotoImage(
    file=relative_to_assets("Decryption_Button.png"))
Decryption_Button = Button(
    background="#363434",
    image=button_image_3,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: Decryption_button_click(),
    relief="flat"
)
Decryption_Button.place(
    x=586.0,
    y=428.0,
    width=121.0,
    height=39.0
)

#------------------Upload Decryption Button-------------------
Upload_Decryption_Button = Button(
    background="#363434",
    image=button_image_2,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: add_content("Decrypted"),
    relief="flat"
)
Upload_Decryption_Button.place(
    x=756.0,
    y=428.0,
    width=40.0,
    height=40.0
)

#------------------Downlaod Decryption Button-------------------
Downlaod_Decryption_Button = Button(
    background="#363434",
    image=button_image_6,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: download("Decrypted"),
    relief="flat"
)
Downlaod_Decryption_Button.place(
    x=816.0,
    y=428.0,
    width=40.0,
    height=40.0
)

#-----------------------Separator-------------------------
canvas.create_rectangle(
    477.996826171875,
    99.0,
    477.99998051789726,
    703.0000109672474,
    fill="#FFFFFF",
    outline="")

#-----------------------Exit Button------------------------
button_image_5 = PhotoImage(
    file=relative_to_assets("Exit_Button.png"))
Exit_Button = Button(
    background="#FF8A00",
    image=button_image_5,
    borderwidth=0,
    highlightthickness=0,
    command=open_Main_window,  # Call the function to open the new window
    relief="flat"
)
Exit_Button.place(
    x=14.0,
    y=8.0,
    width=45.0,
    height=45.0
)

window.resizable(False, False)
window.mainloop()




# import streamlit as st
# import json
# import os
# import base64
# import time
# from datetime import datetime
# from cryptography.fernet import Fernet
# from hashlib import pbkdf2_hmac

# # ---------- CONFIG ----------
# st.set_page_config(page_title="Secure Vault", layout="wide")

# DATA_FILE = "data.json"
# KEY_FILE = "fernet.key"
# LOCKOUT_DURATION = 30  # seconds

# # ---------- SESSION STATES ----------
# if 'users' not in st.session_state:
#     if os.path.exists(DATA_FILE):
#         with open(DATA_FILE, 'r') as f:
#             st.session_state.users = json.load(f)
#     else:
#         st.session_state.users = {}

# if 'current_user' not in st.session_state:
#     st.session_state.current_user = None

# if "attempts" not in st.session_state:
#     st.session_state.attempts = 0

# if "lockout_time" not in st.session_state:
#     st.session_state.lockout_time = 0

# if "page" not in st.session_state:
#     st.session_state.page = "home"

# if "changed" not in st.session_state:
#     st.session_state.changed = False

# # ---------- ENCRYPTION ----------
# def generate_key():
#     key = Fernet.generate_key()
#     with open(KEY_FILE, 'wb') as f:
#         f.write(key)
#     return key

# def load_key():
#     if not os.path.exists(KEY_FILE):
#         return generate_key()
#     with open(KEY_FILE, 'rb') as f:
#         return f.read()

# fernet = Fernet(load_key())

# def hash_pass(password, salt="somesalt"):
#     return base64.b64encode(pbkdf2_hmac('sha256', password.encode(), salt.encode(), 100000)).decode()

# def save_users():
#     with open(DATA_FILE, 'w') as f:
#         json.dump(st.session_state.users, f, indent=4)

# # ---------- AUTH ----------
# def login(username, password):
#     users = st.session_state.users
#     if username in users and users[username]['password'] == hash_pass(password):
#         st.session_state.current_user = username
#         st.session_state.attempts = 0
#         st.session_state.page = "home"
#         return True
#     return False

# def register(username, password):
#     users = st.session_state.users
#     if username not in users:
#         users[username] = {"password": hash_pass(password), "data": []}
#         save_users()
#         return True
#     return False

# # ---------- PAGES ----------
# def login_page():
#     st.markdown("## 🔐 Login or Register")
#     choice = st.radio("Select", ["Login", "Register"], horizontal=True)
#     username = st.text_input("Username")
#     password = st.text_input("Password", type="password")

#     if st.button("Submit"):
#         if choice == "Login":
#             if login(username, password):
#                 st.success("✅ Logged in successfully")
#                 st.rerun()
#             else:
#                 st.error("❌ Invalid credentials")
#         elif choice == "Register":
#             if register(username, password):
#                 st.success("✅ Registered! Now log in.")
#             else:
#                 st.error("⚠️ User already exists")

# def home_page():
#     st.markdown("""
# <div style="background-color:#e3f2fd;padding:25px 20px;border-left:8px solid #fb8c00;border-radius:8px;margin-bottom:30px;">
#   <h2 style="color:#e65100;">🌟 "Your Words, Locked in Silence"</h2>
#   <p style="font-size:17px;line-height:1.6;color:#4e342e;">
#     Every thought you pen, every memory you store, deserves a place safe from judgment, theft, and time. 
#     In this digital world overflowing with noise, there must exist a sanctuary — a vault of silence where your voice stays hidden, yet heard by you alone.
#     <br><br>
#     This isn’t just an app — it’s your companion in confidentiality. With every encrypted word, you're reclaiming control over your privacy.
#     No passwords stored, no data sold, no third-party access — only trust, mathematics, and your chosen key.
#     <br><br>
#     So speak freely. Store boldly. Your secrets are not forgotten — they are simply protected.  
#     <br><br>
#     <em>“Because some messages are meant only for your future self.”</em>
#   </p>
# </div>
# """, unsafe_allow_html=True)

# def insert_page():
#     st.title("➕ Insert Encrypted Data")
#     text = st.text_area("Enter data to encrypt")
#     passkey = st.text_input("Passkey", type="password")
#     if st.button("Encrypt and Save"):
#         if text and passkey:
#             encrypted = fernet.encrypt(text.encode()).decode()
#             hashed = hash_pass(passkey)
#             st.session_state.users[st.session_state.current_user]["data"].append({
#                 "encrypted_text": encrypted,
#                 "passkey": hashed,
#                 "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#             })
#             save_users()
#             st.success("Data saved and encrypted!")
#             st.session_state.changed = True

# def retrieve_page():
#     st.title("🔍 Retrieve Encrypted Data")
#     if st.session_state.attempts >= 3:
#         st.session_state.lockout_time = time.time()
#         st.session_state.page = "locked"
#         st.session_state.changed = True

#     user_data = st.session_state.users[st.session_state.current_user]["data"]
#     if not user_data:
#         st.info("No data available.")
#         return

#     options = [f"{idx + 1}. Saved on: {entry['timestamp']}" for idx, entry in enumerate(user_data)]
#     idx = st.selectbox("Choose Entry", options)

#     selected_entry = user_data[int(idx.split('.')[0]) - 1]
#     st.caption(f"Saved on: {selected_entry['timestamp']}")

#     passkey = st.text_input("Enter Passkey", type="password")

#     if st.button("Decrypt"):
#         if hash_pass(passkey) == selected_entry["passkey"]:
#             decrypted = fernet.decrypt(selected_entry["encrypted_text"].encode()).decode()
#             st.success(f"Decrypted Text: {decrypted}")
#             st.session_state.attempts = 0
#         else:
#             st.session_state.attempts += 1
#             st.error(f"Wrong passkey. Attempts left: {3 - st.session_state.attempts}")

#     if st.button("Delete Entry"):
#         user_data.pop(int(idx.split('.')[0]) - 1)
#         save_users()
#         st.success("Entry deleted.")
#         st.session_state.changed = True

# def lockout_page():
#     elapsed = time.time() - st.session_state.lockout_time
#     if elapsed < LOCKOUT_DURATION:
#         st.error(f"🛑 Too many wrong attempts. Please wait {int(LOCKOUT_DURATION - elapsed)} seconds.")
#     else:
#         st.session_state.attempts = 0
#         st.session_state.page = "retrieve"
#         st.rerun()

# # ---------- SIDEBAR ----------
# def sidebar():
#     with st.sidebar:
#         st.title("🛡️ Secure Vault")
#         if st.session_state.current_user:
#             st.write(f"👤 Logged in as: `{st.session_state.current_user}`")
#             page = st.radio("Navigate", ["🏠 Home", "➕ Insert", "🔍 Retrieve", "🚪 Logout"])
#             if page.startswith("🏠"):
#                 st.session_state.page = "home"
#             elif page.startswith("➕"):
#                 st.session_state.page = "insert"
#             elif page.startswith("🔍"):
#                 st.session_state.page = "retrieve"
#             elif page.startswith("🚪"):
#                 st.session_state.current_user = None
#                 st.session_state.page = "login"
#                 st.rerun()

# # ---------- MAIN ----------
# if st.session_state.current_user is None:
#     login_page()
# else:
#     if "changed" in st.session_state and st.session_state.changed:
#         st.rerun()

#     sidebar()

#     if st.session_state.page == "home":
#         home_page()
#     elif st.session_state.page == "insert":
#         insert_page()
#     elif st.session_state.page == "retrieve":
#         retrieve_page()
#     elif st.session_state.page == "locked":
#         lockout_page()




import streamlit as st
import json
import os
import base64
import time
from datetime import datetime
from cryptography.fernet import Fernet
from hashlib import pbkdf2_hmac

# ---------- CONFIG ----------
st.set_page_config(page_title="Secure Vault", layout="wide")

DATA_FILE = "data.json"
KEY_FILE = "fernet.key"
LOCKOUT_DURATION = 30  # seconds

# ---------- SESSION STATES ----------
if 'users' not in st.session_state:
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            st.session_state.users = json.load(f)
    else:
        st.session_state.users = {}

if 'current_user' not in st.session_state:
    st.session_state.current_user = None

if "attempts" not in st.session_state:
    st.session_state.attempts = 0

if "lockout_time" not in st.session_state:
    st.session_state.lockout_time = 0

if "page" not in st.session_state:
    st.session_state.page = "home"

if "changed" not in st.session_state:
    st.session_state.changed = False

# ---------- ENCRYPTION ----------
def generate_key():
    key = Fernet.generate_key()
    with open(KEY_FILE, 'wb') as f:
        f.write(key)
    return key

def load_key():
    if not os.path.exists(KEY_FILE):
        return generate_key()
    with open(KEY_FILE, 'rb') as f:
        return f.read()

fernet = Fernet(load_key())

def hash_pass(password, salt="somesalt"):
    return base64.b64encode(pbkdf2_hmac('sha256', password.encode(), salt.encode(), 100000)).decode()

def save_users():
    with open(DATA_FILE, 'w') as f:
        json.dump(st.session_state.users, f, indent=4)

# ---------- AUTH ----------
def login(username, password):
    users = st.session_state.users
    if username in users and users[username]['password'] == hash_pass(password):
        st.session_state.current_user = username
        st.session_state.attempts = 0
        st.session_state.page = "home"
        return True
    return False

def register(username, password):
    users = st.session_state.users
    if username not in users:
        users[username] = {"password": hash_pass(password), "data": []}
        save_users()
        return True
    return False

# ---------- PAGES ----------
def login_page():
    st.markdown("## 🔐 Login or Register")
    choice = st.radio("Select", ["Login", "Register"], horizontal=True)
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Submit"):
        if choice == "Login":
            if login(username, password):
                st.success("✅ Logged in successfully")
                st.rerun()
            else:
                st.error("❌ Invalid credentials")
        elif choice == "Register":
            if register(username, password):
                st.success("✅ Registered! Now log in.")
            else:
                st.error("⚠️ User already exists")

def home_page():
    st.markdown("""
<div style="background-color:#e3f2fd;padding:25px 20px;border-left:8px solid #fb8c00;border-radius:8px;margin-bottom:30px;">
  <h2 style="color:#e65100;">🌟 "Your Words, Locked in Silence"</h2>
  <p style="font-size:17px;line-height:1.6;color:#4e342e;">
    Every thought you pen, every memory you store, deserves a place safe from judgment, theft, and time. 
    In this digital world overflowing with noise, there must exist a sanctuary — a vault of silence where your voice stays hidden, yet heard by you alone.
    <br><br>
    This isn’t just an app — it’s your companion in confidentiality. With every encrypted word, you're reclaiming control over your privacy.
    No passwords stored, no data sold, no third-party access — only trust, mathematics, and your chosen key.
    <br><br>
    So speak freely. Store boldly. Your secrets are not forgotten — they are simply protected.  
    <br><br>
    <em>“Because some messages are meant only for your future self.”</em>
  </p>
</div>
""", unsafe_allow_html=True)

def insert_page():
    st.title("➕ Insert Encrypted Data")
    text = st.text_area("Enter data to encrypt")
    passkey = st.text_input("Passkey", type="password")
    if st.button("Encrypt and Save"):
        if text and passkey:
            encrypted = fernet.encrypt(text.encode()).decode()
            hashed = hash_pass(passkey)
            st.session_state.users[st.session_state.current_user]["data"].append({
                "encrypted_text": encrypted,
                "passkey": hashed,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })
            save_users()
            st.success("Data saved and encrypted!")
            st.session_state.changed = True

def retrieve_page():
    st.title("🔍 Retrieve Encrypted Data")
    
    # Check if attempts are more than 3 and apply lockout
    if st.session_state.attempts >= 3:
        st.session_state.lockout_time = time.time()
        st.session_state.page = "locked"
        st.session_state.changed = True
        return  # Skip the rest of the retrieval logic if locked out
    
    user_data = st.session_state.users[st.session_state.current_user]["data"]
    if not user_data:
        st.info("No data available.")
        return

    # Provide a selectbox for choosing saved data
    options = [f"{idx + 1}. Saved on: {entry['timestamp']}" for idx, entry in enumerate(user_data)]
    idx = st.selectbox("Choose Entry", options)

    # Get the selected entry's data
    selected_entry = user_data[int(idx.split('.')[0]) - 1]
    st.caption(f"Saved on: {selected_entry['timestamp']}")

    passkey = st.text_input("Enter Passkey", type="password")

    # Attempt decryption when the button is pressed
    if st.button("Decrypt"):
        if hash_pass(passkey) == selected_entry["passkey"]:
            decrypted = fernet.decrypt(selected_entry["encrypted_text"].encode()).decode()
            st.success(f"Decrypted Text: {decrypted}")
            st.session_state.attempts = 0  # Reset attempts after successful decryption
            st.session_state.changed = True
        else:
            st.session_state.attempts += 1
            st.error(f"Wrong passkey. Attempts left: {3 - st.session_state.attempts}")
    
    # Option to delete an entry
    if st.button("Delete Entry"):
        user_data.pop(int(idx.split('.')[0]) - 1)
        save_users()
        st.success("Entry deleted.")
        st.session_state.changed = True

def lockout_page():
    st.title("🔒 Locked Out")
    st.error("Too many failed attempts. Please try again after 60 seconds.")

    if time.time() - st.session_state.lockout_time >= 60:
        st.session_state.attempts = 0
        st.session_state.page = "home"
        st.success("You can try again now. Returning to Home page.")
        st.session_state.changed = True

# ---------- SIDEBAR ----------
def sidebar():
    with st.sidebar:
        st.title("🛡️ Secure Vault")
        if st.session_state.current_user:
            st.write(f"👤 Logged in as: `{st.session_state.current_user}`")
            page = st.radio("Navigate", ["🏠 Home", "➕ Insert", "🔍 Retrieve", "🚪 Logout"])
            if page.startswith("🏠"):
                st.session_state.page = "home"
            elif page.startswith("➕"):
                st.session_state.page = "insert"
            elif page.startswith("🔍"):
                st.session_state.page = "retrieve"
            elif page.startswith("🚪"):
                st.session_state.current_user = None
                st.session_state.page = "login"
                st.rerun()

# ---------- MAIN ----------
if st.session_state.current_user is None:
    login_page()
else:
    if "changed" in st.session_state and st.session_state.changed:
        st.rerun()

    sidebar()

    if st.session_state.page == "home":
        home_page()
    elif st.session_state.page == "insert":
        insert_page()
    elif st.session_state.page == "retrieve":
        retrieve_page()
    elif st.session_state.page == "locked":
        lockout_page()

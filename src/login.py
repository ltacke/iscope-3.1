# login.py

import streamlit as st
import yaml
import streamlit_authenticator as stauth
from yaml.loader import SafeLoader


def load_config():
    """Load configuration file for authentication settings."""
    with open("src/backend/config.yaml") as file:
        return yaml.load(file, Loader=SafeLoader)


def setup_authenticator():
    """Set up the Streamlit authenticator using configuration data."""
    config = load_config()
    authenticator = stauth.Authenticate(
        config["credentials"],
        config["cookie"]["name"],
        config["cookie"]["key"],
        config["cookie"]["expiry_days"],
    )
    return authenticator


def login(authenticator):
    """Handle user login and authentication."""
    try:
        authenticator.login()
    except Exception as e:
        st.error(e)

    return st.session_state.get("authentication_status")


def logout(authenticator):
    """Handle user logout."""
    authenticator.logout("Logout", "sidebar")


# This will be used to set up the authenticator and check login status in main.py

import streamlit as st
import pandas as pd
import base64
import time

# Define valid usernames and passwords
valid_credentials = {
    "user1": "1111",
    "user2": "password2"
}

def split_text(text):
    # function to split text into words
    try:
        words = text.split()
    except:
        return None
    return words

def main():
    # Check if the user is already logged in
    if "username" not in st.session_state:
        st.session_state.username = None

    # If the user is not logged in, show the login page
    if st.session_state.username is None:
        st.title("Data Transformation Bot Login")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        login_button = st.button("Login")

        # If the user clicks the login button, check their credentials
        if login_button:
            if username in valid_credentials and password == valid_credentials[username]:
                # If the credentials are valid, log the user in
                st.session_state.username = username
                st.success("Logged in as " + username)

    # If the user is logged in, show the main page
    if st.session_state.username is not None:
        st.title("Data Transformation Bot")
        
        # option to enter text manually
        manual_text = st.text_area("One Case Example")
        manual_button = st.button("Normalize")
        # if manual text is entered, display a button for generating the results
        if manual_text and manual_button:
            words = split_text(manual_text)
            st.write(words)

        # option to upload a file
        uploaded_file = st.file_uploader("Upload Data")

        # if a file is uploaded, display the contents
        if uploaded_file is not None:
            # read the file into a pandas dataframe
            file = pd.ExcelFile(uploaded_file)
            sheet_names = file.sheet_names
            sheet_name = st.selectbox("Select sheet", sheet_names)

            df = pd.read_excel(uploaded_file, sheet_name=sheet_name)

            st.write("First 5 rows of the selected sheet:")
            st.write(df.head())

            # get the name of the text column to split
            text_column = st.selectbox("Select Product Description Column to Normalize", df.columns)

            # display a button to run the splitting process
            if st.button("Run"):
                start_time = time.time()
                with st.spinner('Processing data...'):
                    df['split_text'] = df[text_column].apply(split_text)

                # allow the user to download the new dataset
                csv = df.to_csv(index=False)
                b64 = base64.b64encode(csv.encode()).decode()
                st.markdown(f'<a href="data:file/csv;base64,{b64}" download="new_dataset.csv">Download CSV</a>', unsafe_allow_html=True)

                elapsed_time = time.time() - start_time
                st.write(f'Time elapsed: {elapsed_time:.2f} seconds')

# Run the app
if __name__ == '__main__':
    main()

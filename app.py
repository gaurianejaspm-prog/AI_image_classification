import streamlit as st

st.title('Welcome to streamlit')

#inputs

m1 = st.text_input('Enter your input')
st.markdown(m1)

m2 = st.text_area('Enter your input')
st.markdown(m2)

st.warning('Please enter your Input')

st.success('updated successfully')

m3 = st.selectbox('Please select',['Python','Java','SQL'])
st.markdown(m3)

m4 = st.multiselect('Please select',['Python','Java','SQL'])
st.markdown(m4)

st.radio('Please select',['Python','Java','SQL'])

st.sidebar.text_input('Enter your name')
st.sidebar.selectbox('Please select',['Python','Java','SQL'])
st.sidebar.radio('Please select',['Python','Java','SQL'])
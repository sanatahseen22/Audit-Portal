import io
import streamlit as st
import pandas as pd
from googletrans import Translator
import streamlit.components.v1 as components

# Set the page configuration
st.set_page_config(page_title='Audit Portal', layout='wide')

# Initialize the Google Translator
translator = Translator()


# Define the task status options
task_status_options = ['Fixed', 'Not Fixed', 'Correct']
# Define the comments options for 'Fixed' and 'Not Fixed' task status
fixed_comments = ['Image', 'Item_name', 'Bullets', 'Product_Description', 'Technical Details', 'QnA', 'Competitor Website', 'Brand Website', 'Hierarchy']
not_fixed_comments = ['Value unavailable', 'Invalid ASIN', 'Misclassified - Different Product', 'Misclassified - Accessory', 'Inconsistent', 'Partial values', 'Not Applicable', 'Clarity Needed']



# File uploader to allow users to select their input file
uploaded_file = st.file_uploader("Upload your input Excel file", type=["xlsx"])

if uploaded_file is not None:
    # Load the input data from the uploaded file
    input_data = pd.read_excel(uploaded_file)

    # Define the columns and their accepted values
    column_details = {
        'ASIN': input_data['ASIN'].tolist(),
        'Product_type': input_data['Product_type'].tolist(),
        'Attribute': input_data['Attribute'].tolist(),
        'Marketplace': input_data['Marketplace'].tolist(),
        'Keywords': input_data['Keywords'].tolist(),
        'Accepted_Values': input_data['Accepted_Values'].tolist(),
        'Attribute_Datatype': input_data['Attribute_Datatype'].tolist(),
        'Image_link': input_data['Image_link'].tolist(),
        'Item_name': input_data['Item_name'].tolist(),
        'Bullet_Point': input_data['Bullet_Point'].tolist(),
        'Product_Description': input_data['Product_Description'].tolist()
    }
    
    # Define the task status options
    task_status_options = ['Fixed', 'Not Fixed', 'Correct']

    # Define the comments options for 'Fixed' and 'Not Fixed' task status
    fixed_comments = ['Image', 'Item_name', 'Bullets', 'Product_Description', 'Technical Details', 'QnA', 'Competitor Website', 'Brand Website', 'Hierarchy']
    not_fixed_comments = ['Value unavailable', 'Invalid ASIN', 'Misclassified - Different Product', 'Misclassified - Accessory', 'Inconsistent', 'Partial values', 'Not Applicable', 'Clarity Needed']





    # Define other necessary functions like `render_image_carousel`, `initialize_session_state`, `save_row`, etc.
    # as you have them in your existing code.
    
    # Function to create the carousel for images using Slick
    def render_image_carousel(image_links):
        # Filter out empty or non-functioning links (basic validation for empty strings)
        valid_links = [img.strip() for img in image_links if img.strip()]

        # If there are valid image links, render the carousel
        if valid_links:
            carousel_html = f"""
            <link rel="stylesheet" type="text/css" href="https://cdn.jsdelivr.net/npm/slick-carousel@1.8.1/slick/slick.css"/>
            <link rel="stylesheet" type="text/css" href="https://cdn.jsdelivr.net/npm/slick-carousel@1.8.1/slick/slick-theme.css"/>
            <script type="text/javascript" src="https://cdn.jsdelivr.net/npm/jquery@3.5.1/dist/jquery.min.js"></script>
            <script type="text/javascript" src="https://cdn.jsdelivr.net/npm/slick-carousel@1.8.1/slick/slick.min.js"></script>

            <div class="carousel">
                {''.join([f'<div><img src="{img}" style="width:400px;height:auto;"/></div>' for img in valid_links])}
            </div>

            <script type="text/javascript">
                $(document).ready(function() {{
                    $('.carousel').slick({{
                        infinite: true,
                        slidesToShow: 1,
                        slidesToScroll: 1,
                        arrows: true,
                        autoplay: true,
                        autoplaySpeed: 1000,
                    }});
                }});
            </script>
            """
            components.html(carousel_html, height=350)

        # If no valid image links, display a placeholder
        else:
            st.markdown("""
                <div style="width:300px;height:200px;display:flex;align-items:center;justify-content:center;border:1px solid #ccc;">
                    <p>No images available</p>
                </div>
            """, unsafe_allow_html=True)


    # Function to initialize session state values before rendering widgets
    def initialize_session_state(index):
        if f'task_status_{index}' not in st.session_state:
            st.session_state[f'task_status_{index}'] = 'Not Fixed'
        if f'attribute_value_{index}' not in st.session_state:
            st.session_state[f'attribute_value_{index}'] = ''
        if f'attribute_unit_{index}' not in st.session_state:
            st.session_state[f'attribute_unit_{index}'] = ''
        if f'comments_{index}' not in st.session_state:
            st.session_state[f'comments_{index}'] = 'Value unavailable'
        if f'third_party_link_{index}' not in st.session_state:
            st.session_state[f'third_party_link_{index}'] = ''
            
    # Function to save data directly into a downloadable Excel file
    def save_row(index):
        # Add new columns to input_data if they don't exist
        columns_to_add = ['Task_Status', 'Task_Comments', 'Attribute_Value', 'D', 'W', 'H', 'T', 'Unit', 'Comments', '3P_Website_Link']
        for col in columns_to_add:
            if col not in input_data.columns:
                input_data[col] = ''
    
        # Update the input_data DataFrame with the new values
        input_data.at[index, 'Task_Status'] = st.session_state[f'task_status_{index}']
        input_data.at[index, 'Task_Comments'] = st.session_state[f'comments_{index}']
        input_data.at[index, 'Attribute_Value'] = st.session_state[f'attribute_value_{index}']
        input_data.at[index, 'D'] = st.session_state[f'D_{index}']
        input_data.at[index, 'W'] = st.session_state[f'W_{index}']
        input_data.at[index, 'H'] = st.session_state[f'H_{index}']
        input_data.at[index, 'T'] = st.session_state[f'T_{index}']
        input_data.at[index, 'Unit'] = st.session_state[f'attribute_unit_{index}']
        input_data.at[index, 'Comments'] = st.session_state[f'task_comment_{index}']
        input_data.at[index, '3P_Website_Link'] = st.session_state[f'third_party_link_{index}']
    
        # Save the updated input_data to an in-memory BytesIO object
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            input_data.to_excel(writer, index=False, sheet_name='Sheet1')
        output.seek(0)
    
        # Provide a download button to save the updated file
        st.download_button(
            label="Download updated file",
            data=output,
            file_name="Updated_Input.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    
        st.success(f"Row {index+1}: Data saved successfully! You can download the updated file.")
        


    # Function to render individual rows
    def render_row(index):
        initialize_session_state(index)

        # Display Item Name with subheading
        st.subheader('Item Name')
        st.markdown(f'''
        <div style="font-size: 18px; font-weight: bold;" class="item-name">
            {translate_text(input_data["Item_name"][index])}
        </div>
    ''', unsafe_allow_html=True)

        # Extract image links from the Image_link column (assuming links are separated by commas)
        image_links = input_data['Image_link'][index].split(',')

        # Layout for Image Carousel and ASIN Info Box
        col_image, col_info = st.columns([1, 1])  # Image carousel on the left, ASIN Info on the right

        with col_image:
            # Render the image carousel
            render_image_carousel(image_links)

        with col_info:
            # ASIN Info Box 
            asin_hyperlink = create_hyperlink(column_details['ASIN'][index], column_details['Marketplace'][index])
            st.markdown(f"""
               <div style="border: 4px solid #ccc; padding: 20px; margin-top: 10px;">
                   <strong>ASIN:</strong> {asin_hyperlink} <br>
                   <strong>Product Type:</strong> {column_details['Product_type'][index]}<br>
                   <strong>Marketplace:</strong> {column_details['Marketplace'][index]}<br>
                   <strong>Attribute:</strong> {column_details['Attribute'][index]}<br>
                   <strong>Keywords:</strong> {column_details['Keywords'][index]}<br>
                   <strong>Attribute_Datatype:</strong> {input_data['Attribute_Datatype'][index]}<br>
                   <strong>Accepted Values:</strong> {column_details['Accepted_Values'][index]}
               </div>
            """, unsafe_allow_html=True)

        # Layout for Product Description
        st.subheader('Bullet Point')
        st.markdown(f'''
        <p style="font-size: 18px;">
            {translate_text(input_data["Bullet_Point"][index])}
        </p>
    ''', unsafe_allow_html=True)

        # Layout for Bullet Points
        st.subheader('Product Description')
        st.markdown(f'''
        <p style="font-size: 18px;">
            {translate_text(input_data["Product_Description"][index])}
        </p>
    ''', unsafe_allow_html=True)

        # Bottom Section 
        col_value, col_d, col_w, col_h, col_t = st.columns([2, 1, 1, 1, 1])
        with col_value:
            st.text_input('Value:', key=f'attribute_value_{index}')
        with col_d:
            st.text_input('D:', key=f'D_{index}')
        with col_w:
            st.text_input('W:', key=f'W_{index}')
        with col_h:
            st.text_input('H:', key=f'H_{index}')
        with col_t:
            st.text_input('T:', key=f'T_{index}')
        
        # 3rd Row for Unit and Comments fields
        col_unit, col_task_comments = st.columns([2, 6])
        with col_unit:
            st.text_input('Unit:', key=f'attribute_unit_{index}')
        
        with col_task_comments:
            st.text_input('Comments:', key=f'task_comment_{index}')

        # Task Status, Comments, and 3P Website Link (in the next row)
        col_status, col_comments, col_website = st.columns([2, 4, 6])

        with col_status:
            st.selectbox('Task Status', task_status_options, key=f'task_status_{index}')
        
        with col_comments:
            if st.session_state[f'task_status_{index}'] == 'Fixed':
                st.selectbox('Task Comments', fixed_comments, key=f'comments_{index}')
            else:
                st.selectbox('Task Comments', not_fixed_comments, key=f'comments_{index}')
        
        with col_website:
            st.text_input('3P Website Link', key=f'third_party_link_{index}')
        
        # Submit Button
        if st.button(f'Submit Row {index+1}'):
            # Validation logic remains the same
            if st.session_state[f'task_status_{index}'] in ['Fixed', 'Correct']:
                if column_details['Attribute_Datatype'][index] == 'Value+Unit':
                    # Parse accepted values for units from column_details
                    accepted_units = column_details['Accepted_Values'][index].split(',')
                    # Check if Value, D, W, H, or T fields are empty
                    if not st.session_state[f'attribute_value_{index}'].strip() and not st.session_state[f'D_{index}'].strip() and not st.session_state[f'W_{index}'].strip() and not st.session_state[f'H_{index}'].strip() and not st.session_state[f'T_{index}'].strip():
                        st.error(f"Row {index+1}: One of Value, D, W, H, or T must be filled!")
                    # Check if the Unit field is empty or invalid
                    elif not st.session_state[f'attribute_unit_{index}'].strip():
                        st.error(f"Row {index+1}: Unit cannot be empty!")
                    elif st.session_state[f'attribute_unit_{index}'].strip() not in accepted_units:
                        st.error(f"Row {index+1}: Unit must be one of the accepted values: {', '.join(accepted_units)}")
                    else:
                        save_row(index)  # Save the row if validation passes
                elif column_details['Attribute_Datatype'][index] in ['String', 'Values Only']:
                    if not st.session_state[f'attribute_value_{index}'].strip():
                        st.error(f"Row {index+1}: Value cannot be empty!")
                    else:
                        save_row(index)  # Save the row if validation passes
            elif st.session_state[f'task_status_{index}'] == 'Not Fixed' and st.session_state[f'comments_{index}'] in ['Value unavailable', 'Invalid ASIN', 'Misclassified - Different Product', 'Misclassified - Accessory', 'Inconsistent', 'Not Applicable']:
                if any([st.session_state[f'attribute_value_{index}'].strip(), st.session_state[f'D_{index}'].strip(), st.session_state[f'W_{index}'].strip(), st.session_state[f'H_{index}'].strip(), st.session_state[f'T_{index}'].strip(), st.session_state[f'attribute_unit_{index}'].strip()]):
                    st.error(f"Row {index+1}: All fields must be empty for 'Not Fixed' with the selected Task Comments!")
                else:
                    save_row(index)  # Save the row if validation passes
            else:
                save_row(index)  # Save without validation if no specific conditions apply


    # Function to translate text
    @st.cache_data
    def translate_text(text):
        if pd.isnull(text):
            return ""
        try:
            return translator.translate(text, src='auto', dest='en').text
        except Exception as e:
            return text

    # Function to determine the correct domain based on the marketplace
    def get_amazon_domain(marketplace):
        if marketplace == "US":
            return "amazon.com"
        elif marketplace == "JP":
            return "amazon.co.jp"
        elif marketplace == "UK":
            return "amazon.co.uk"
        elif marketplace in ["BR", "MX", "AU", "TR", "BE", "CO", "NG"]:
            return f"amazon.com.{marketplace.lower()}"
        else:
            return f"www.amazon.{marketplace.lower()}"

    # Function to create a hyperlink for each ASIN based on the marketplace
    def create_hyperlink(asin, marketplace):
        domain = get_amazon_domain(marketplace)
        url = f"https://{domain}/dp/{asin}"
        return f'<a href="{url}" target="_blank">{asin}</a>'


    # Main function for the Streamlit app
    def main():
        # Display 20 rows per page
        rows_per_page = 20
        current_page = st.session_state.get('current_page', 0)

        # Calculate the starting and ending indices for the current page
        start_index = current_page * rows_per_page
        end_index = min(start_index + rows_per_page, len(input_data))

        for i in range(start_index, end_index):
            render_row(i)
            st.markdown("---")

        # Pagination buttons
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button('Previous Page'):
                if current_page > 0:
                    st.session_state['current_page'] = current_page - 1
        with col2:
            st.write(f"Page {current_page + 1}")
        with col3:
            if st.button('Next Page'):
                if end_index < len(input_data):
                    st.session_state['current_page'] = current_page + 1

    # Call the main function
    if __name__ == "__main__":
        main()

else:
    st.warning("Please upload an input Excel file to proceed.")


from dotenv import load_dotenv
load_dotenv()
import streamlit as st
from crewai import Agent, Crew
from tasks import MarketingAnalysisTasks
from agents import MarketingAnalysisAgents
import logging
import io
import time
import images

# Function to get logs from the log stream
log_filename = 'app.log'
logging.basicConfig(level=logging.DEBUG, filename=log_filename, filemode='a', format='%(asctime)s - %(levelname)s - %(message)s')


def main():
    
    
    # Load images
    banner_image = "images/NathcorpLogo-Text-side_400x53.png"  # Replace with your banner image path
    logo_image = "images\png-transparent-goal-definition-product-marketing-do-not-care-text-logo-plan.png"  # Replace with your logo image path
    # Display banner image
    st.image(banner_image, use_column_width=True)
    # Create columns for logo, title, and dropdown
    col1, col2, col3 = st.columns([1, 6, 1])
    
    # Display logo image in the first column
    with col1:
        st.image(logo_image, width=60)
    # Display title in the second column
    with col2:
        st.title("Marketing Crew: Product Marketing Strategy Generator")
    # Display model selection dropdown in the third column
    with col3:
        st.write(" ")  # Add some space
        model = st.selectbox("Select OpenAI Model", ["GPT-3.5", "GPT-4"], key='model_dropdown')
    
    
    # st.title("Marketing Crew: Product Marketing Strategy Generator")
    st.write("Welcome to the Marketing Crew! Input your product details below to generate a marketing strategy.")
    # Input product details
    product_website = st.text_input("Product Website", "")
    product_details = st.text_area("Product Details / Instagram Post Description", "")
    if st.button("Generate Marketing Strategy"):
        
        # Initialize tasks and agents
        tasks = MarketingAnalysisTasks()
        agents = MarketingAnalysisAgents()
        
        # Create Agents
        product_competitor_agent = agents.product_competitor_agent()
        strategy_planner_agent = agents.strategy_planner_agent()
        creative_agent = agents.creative_content_creator_agent()
        
        # Create Tasks
        website_analysis = tasks.product_analysis(product_competitor_agent, product_website, product_details)
        market_analysis = tasks.competitor_analysis(product_competitor_agent, product_website, product_details)
        campaign_development = tasks.campaign_development(strategy_planner_agent, product_website, product_details)
        write_copy = tasks.instagram_ad_copy(creative_agent)
        
        # Create Crew responsible for Copy
        copy_crew = Crew(
            agents=[product_competitor_agent, strategy_planner_agent, creative_agent],
            tasks=[website_analysis, market_analysis, campaign_development],
            verbose=True
        )
        with st.spinner("Generating marketing strategy..."):
            ad_copy = copy_crew.kickoff()
            
            
        insta_crew = Crew(
            agents=[product_competitor_agent, strategy_planner_agent, creative_agent, creative_agent],
            tasks=[website_analysis, market_analysis, campaign_development, write_copy],
            verbose=True
        )    
        with st.spinner("Generating Insta Post for social media marketing..."):
            ad_post = insta_crew.kickoff()
            
        # Create Crew responsible for Image
        senior_photographer = agents.senior_photographer_agent()
        chief_creative_director = agents.chief_creative_director_agent()
        
        # # Create Tasks for Image
        take_photo = tasks.take_photograph_task(senior_photographer, ad_copy, product_website, product_details)
        approve_photo = tasks.review_photo(chief_creative_director, product_website, product_details)
        image_crew = Crew(
            agents=[senior_photographer, chief_creative_director],
            tasks=[take_photo, approve_photo],
            verbose=True
        )
        
        #   Run Image Crew
        with st.spinner("Generating image..."):
            image = image_crew.kickoff()
        
        st.header("Marketing Strategy Results:")
        # st.subheader("Your Post Copy:")
        st.write(ad_copy)
        st.subheader("Your 3 Post suggestion for Instagram:")
        st.write(ad_post)
        st.subheader("Your Midjourney Description:")
        st.write(image)
        
        
        
        
        
        # Display results
    
        
        
        
        # Button to generate new log entries (for demonstration purposes)
        # if st.button("Generate Log Entry"):
        #     logging.info("This is a new log entry generated by the user.")
        # unique_value = 0
        # # Continuous update of logs every second
        # while True:
        #     unique_value += 1
        #     logs = get_logs(log_stream)
        #     log_placeholder.text_area("logs", logs, height=400, key=f"logs{unique_value}")
        #     time.sleep(1)
        
        # #   Display logs in UI
        # st.header("Execution Logs:")
        # with open('app.log', 'r') as f:
        #     logs = f.readlines()
        #     for log in logs:
        #         st.text(log.strip())
        
        
if __name__ == "__main__":
    main()

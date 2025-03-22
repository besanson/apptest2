import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from PIL import Image
import random

# Set page configuration
st.set_page_config(
    page_title="Consumer Insights AI Advisor",
    page_icon="👥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Add custom CSS
st.markdown("""
<style>
    .main {
        background-color: #f5f7f9;
    }
    .consumer-card {
        background-color: white;
        border-radius: 10px;
        padding: 20px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin-bottom: 20px;
    }
    .st-emotion-cache-1r6slb0 {
        background-color: #e9eff5;
    }
    .stButton>button {
        background-color: #4e89ae;
        color: white;
        border-radius: 5px;
        border: none;
        padding: 10px 24px;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state variables
if 'consumer_profiles' not in st.session_state:
    # Create some example consumer profiles
    st.session_state.consumer_profiles = [
        {
            "id": 1,
            "name": "Emily Chen",
            "age": 28,
            "occupation": "Marketing Manager",
            "income": "$75,000",
            "location": "Urban",
            "interests": ["Fitness", "Sustainable products", "Travel"],
            "pain_points": ["Lack of time", "Price sensitivity", "Wants eco-friendly options"],
            "spending_habits": "Prefers quality over quantity, researches before purchasing",
            "avatar": "👩‍💼",
            "buying_stage": "Consideration"
        },
        {
            "id": 2,
            "name": "James Wilson",
            "age": 42,
            "occupation": "IT Professional",
            "income": "$95,000",
            "location": "Suburban",
            "interests": ["Technology", "Home improvement", "Gaming"],
            "pain_points": ["Feature complexity", "Technical support", "Value for money"],
            "spending_habits": "Early adopter, willing to pay premium for latest tech",
            "avatar": "👨‍💻",
            "buying_stage": "Awareness"
        },
        {
            "id": 3,
            "name": "Maria Rodriguez",
            "age": 35,
            "occupation": "Healthcare Worker",
            "income": "$62,000",
            "location": "Urban",
            "interests": ["Cooking", "Family activities", "Health & wellness"],
            "pain_points": ["Limited free time", "Product reliability", "Family budget constraints"],
            "spending_habits": "Practical buyer, looks for deals and family-oriented products",
            "avatar": "👩‍⚕️",
            "buying_stage": "Decision"
        }
    ]

if 'selected_profile' not in st.session_state:
    st.session_state.selected_profile = None

if 'advice_history' not in st.session_state:
    st.session_state.advice_history = []

if 'products' not in st.session_state:
    # Example product data
    st.session_state.products = [
        {"name": "Premium Fitness Tracker", "category": "Fitness", "price": 129.99, "eco_friendly": True},
        {"name": "Smart Home Hub", "category": "Technology", "price": 199.99, "eco_friendly": False},
        {"name": "Organic Meal Kit Subscription", "category": "Cooking", "price": 12.99, "eco_friendly": True},
        {"name": "Professional Laptop", "category": "Technology", "price": 1299.99, "eco_friendly": False},
        {"name": "Eco-Friendly Water Bottle", "category": "Sustainable products", "price": 24.99, "eco_friendly": True},
        {"name": "Family Board Game Set", "category": "Family activities", "price": 34.99, "eco_friendly": True}
    ]

# Sidebar - App navigation
st.sidebar.title("Consumer Insights AI")
st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/d/d5/Poesia_-_logo_%28Italy%2C_2020%29.svg", width=150)  # Replace with your logo

# Create tabs for different sections
page = st.sidebar.radio("Navigation", [
    "🏠 Dashboard", 
    "👥 Consumer Profiles", 
    "🤖 AI Consumer Advisor",
    "📊 Insights & Analytics",
    "⚙️ Settings"
])

# Main content area
if page == "🏠 Dashboard":
    st.title("Consumer Insights AI Dashboard")
    st.subheader("Welcome to your digital consumer advisor")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="consumer-card">
            <h3>👥 Active Consumer Profiles</h3>
            <p>Currently simulating {0} consumer personas</p>
            <p>Last updated: Today</p>
        </div>
        """.format(len(st.session_state.consumer_profiles)), unsafe_allow_html=True)
        
        st.markdown("""
        <div class="consumer-card">
            <h3>🧠 Recent Insights</h3>
            <ul>
                <li>Eco-friendly product interest up 23% among urban consumers</li>
                <li>Tech-savvy segments showing price sensitivity in Q1</li>
                <li>Family-oriented consumers prioritizing value over features</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        # Sample visualization
        st.markdown("<div class='consumer-card'>", unsafe_allow_html=True)
        st.subheader("Consumer Interests Distribution")
        
        # Gather all interests from profiles
        all_interests = []
        for profile in st.session_state.consumer_profiles:
            all_interests.extend(profile["interests"])
        
        interest_counts = pd.Series(all_interests).value_counts()
        
        fig, ax = plt.subplots(figsize=(8, 5))
        sns.barplot(x=interest_counts.index, y=interest_counts.values, ax=ax)
        plt.xticks(rotation=45)
        plt.tight_layout()
        st.pyplot(fig)
        st.markdown("</div>", unsafe_allow_html=True)

elif page == "👥 Consumer Profiles":
    st.title("Digital Consumer Profiles")
    st.write("Browse and manage your digital consumer personas.")
    
    # Display existing profiles in a grid
    cols = st.columns(3)
    for i, profile in enumerate(st.session_state.consumer_profiles):
        with cols[i % 3]:
            st.markdown(f"""
            <div class="consumer-card">
                <center><h1>{profile['avatar']}</h1></center>
                <h3>{profile['name']}, {profile['age']}</h3>
                <p><b>Occupation:</b> {profile['occupation']}</p>
                <p><b>Income:</b> {profile['income']}</p>
                <p><b>Location:</b> {profile['location']}</p>
                <p><b>Buying Stage:</b> {profile['buying_stage']}</p>
                <p><b>Interests:</b> {', '.join(profile['interests'])}</p>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button(f"Edit {profile['name']}", key=f"edit_{profile['id']}"):
                st.session_state.selected_profile = profile
    
    # Add new profile button
    if st.button("+ Add New Consumer Profile"):
        st.session_state.selected_profile = {
            "id": len(st.session_state.consumer_profiles) + 1,
            "name": "",
            "age": 30,
            "occupation": "",
            "income": "",
            "location": "",
            "interests": [],
            "pain_points": [],
            "spending_habits": "",
            "avatar": "👤",
            "buying_stage": "Awareness"
        }
    
    # Profile editor
    if st.session_state.selected_profile:
        st.subheader("Edit Consumer Profile")
        
        col1, col2 = st.columns(2)
        
        with col1:
            name = st.text_input("Name", value=st.session_state.selected_profile.get("name", ""))
            age = st.number_input("Age", min_value=18, max_value=100, value=st.session_state.selected_profile.get("age", 30))
            occupation = st.text_input("Occupation", value=st.session_state.selected_profile.get("occupation", ""))
            income = st.text_input("Income", value=st.session_state.selected_profile.get("income", ""))
            location = st.selectbox("Location", ["Urban", "Suburban", "Rural"], 
                                   index=["Urban", "Suburban", "Rural"].index(st.session_state.selected_profile.get("location", "Urban")) if st.session_state.selected_profile.get("location") else 0)
        
        with col2:
            avatar_options = ["👤", "👩‍💼", "👨‍💼", "👩‍⚕️", "👨‍⚕️", "👩‍🏫", "👨‍🏫", "👩‍💻", "👨‍💻", "👩‍🍳", "👨‍🍳"]
            avatar = st.selectbox("Avatar", avatar_options, 
                                 index=avatar_options.index(st.session_state.selected_profile.get("avatar", "👤")) if st.session_state.selected_profile.get("avatar") in avatar_options else 0)
            
            buying_stage = st.selectbox("Buying Stage", ["Awareness", "Consideration", "Decision"], 
                                       index=["Awareness", "Consideration", "Decision"].index(st.session_state.selected_profile.get("buying_stage", "Awareness")) if st.session_state.selected_profile.get("buying_stage") else 0)
            
            interests = st.multiselect("Interests", 
                                      ["Fitness", "Technology", "Cooking", "Travel", "Family activities", "Gaming", "Reading", "Music", "Sustainable products", "Health & wellness", "Home improvement"],
                                      default=st.session_state.selected_profile.get("interests", []))
            
            pain_points = st.multiselect("Pain Points", 
                                        ["Lack of time", "Price sensitivity", "Feature complexity", "Technical support", "Product reliability", "Family budget constraints", "Value for money", "Wants eco-friendly options"],
                                        default=st.session_state.selected_profile.get("pain_points", []))
        
        spending_habits = st.text_area("Spending Habits", value=st.session_state.selected_profile.get("spending_habits", ""))
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Save Profile"):
                # Update the profile in session state
                updated_profile = {
                    "id": st.session_state.selected_profile["id"],
                    "name": name,
                    "age": age,
                    "occupation": occupation,
                    "income": income,
                    "location": location,
                    "interests": interests,
                    "pain_points": pain_points,
                    "spending_habits": spending_habits,
                    "avatar": avatar,
                    "buying_stage": buying_stage
                }
                
                # Find and update the profile in the list, or add new one
                found = False
                for i, profile in enumerate(st.session_state.consumer_profiles):
                    if profile["id"] == updated_profile["id"]:
                        st.session_state.consumer_profiles[i] = updated_profile
                        found = True
                        break
                
                if not found:
                    st.session_state.consumer_profiles.append(updated_profile)
                
                st.session_state.selected_profile = None
                st.success("Profile saved successfully!")
                st.experimental_rerun()
        
        with col2:
            if st.button("Cancel"):
                st.session_state.selected_profile = None
                st.experimental_rerun()

elif page == "🤖 AI Consumer Advisor":
    st.title("AI Consumer Advisor")
    st.write("Get personalized advice based on consumer profiles.")
    
    # Select a consumer profile
    selected_profile_id = st.selectbox(
        "Select Consumer Profile",
        options=[p["id"] for p in st.session_state.consumer_profiles],
        format_func=lambda x: next((p["name"] for p in st.session_state.consumer_profiles if p["id"] == x), "")
    )
    
    selected_profile = next((p for p in st.session_state.consumer_profiles if p["id"] == selected_profile_id), None)
    
    if selected_profile:
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.markdown(f"""
            <div class="consumer-card">
                <center><h1>{selected_profile['avatar']}</h1></center>
                <h3>{selected_profile['name']}, {selected_profile['age']}</h3>
                <p><b>Occupation:</b> {selected_profile['occupation']}</p>
                <p><b>Income:</b> {selected_profile['income']}</p>
                <p><b>Location:</b> {selected_profile['location']}</p>
                <p><b>Buying Stage:</b> {selected_profile['buying_stage']}</p>
                <p><b>Interests:</b> {', '.join(selected_profile['interests'])}</p>
                <p><b>Pain Points:</b> {', '.join(selected_profile['pain_points'])}</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.subheader("What would you like advice on?")
            
            advice_type = st.selectbox(
                "Advice Type",
                ["Product Recommendations", "Marketing Messaging", "Pricing Strategy", "Customer Experience", "Feature Prioritization"]
            )
            
            category = st.selectbox(
                "Product Category",
                ["All Categories", "Fitness", "Technology", "Cooking", "Family activities", "Sustainable products"]
            )
            
            if st.button("Generate Advice"):
                with st.spinner("Analyzing consumer profile..."):
                    # Simulate processing time
                    progress_bar = st.progress(0)
                    for i in range(100):
                        progress_bar.progress(i + 1)
                        import time
                        time.sleep(0.01)
                    
                    # Generate advice based on profile and selected options
                    if advice_type == "Product Recommendations":
                        # Filter products by category and interests
                        relevant_products = []
                        for product in st.session_state.products:
                            if (category == "All Categories" or product["category"] == category) and \
                               (product["category"] in selected_profile["interests"] or \
                                (product["eco_friendly"] and "Sustainable products" in selected_profile["interests"])):
                                relevant_products.append(product)
                        
                        # Sort by relevance (simplistic approach for demo)
                        if "Price sensitivity" in selected_profile["pain_points"]:
                            relevant_products.sort(key=lambda x: x["price"])
                        
                        # Generate advice
                        advice = {
                            "type": advice_type,
                            "date": "Today",
                            "content": f"Based on {selected_profile['name']}'s profile, I recommend focusing on these products:\n\n"
                        }
                        
                        if relevant_products:
                            for product in relevant_products[:3]:
                                eco_label = " (Eco-friendly)" if product["eco_friendly"] else ""
                                advice["content"] += f"- {product['name']}{eco_label}: ${product['price']}\n"
                            
                            # Add rationale
                            advice["content"] += f"\nRationale: These products align with {selected_profile['name']}'s interests in {', '.join(selected_profile['interests'][:2])}. "
                            
                            if "Price sensitivity" in selected_profile["pain_points"]:
                                advice["content"] += "I've prioritized more affordable options due to price sensitivity. "
                            
                            if "Wants eco-friendly options" in selected_profile["pain_points"] and any(p["eco_friendly"] for p in relevant_products[:3]):
                                advice["content"] += "I've included eco-friendly options as requested. "
                            
                            advice["content"] += f"\n\nFor this {selected_profile['buying_stage'].lower()} stage consumer, emphasize "
                            
                            if selected_profile["buying_stage"] == "Awareness":
                                advice["content"] += "how these products solve specific problems they face."
                            elif selected_profile["buying_stage"] == "Consideration":
                                advice["content"] += "comparative benefits and unique features."
                            else:  # Decision
                                advice["content"] += "social proof, guarantees, and easy purchasing process."
                        else:
                            advice["content"] += "No specific products match the criteria. Consider expanding your product catalog to include items related to " + ", ".join(selected_profile["interests"]) + "."
                    
                    elif advice_type == "Marketing Messaging":
                        # Generate messaging advice
                        advice = {
                            "type": advice_type,
                            "date": "Today",
                            "content": f"Recommended messaging approach for {selected_profile['name']}:\n\n"
                        }
                        
                        # Tailor by buying stage
                        if selected_profile["buying_stage"] == "Awareness":
                            advice["content"] += "Focus on problem identification and education. Use messaging that helps this consumer recognize the challenges they face.\n\n"
                            advice["content"] += "Suggested headlines:\n"
                            advice["content"] += f"- \"How {selected_profile['occupation']}s Save Time While Maximizing Results\"\n"
                            advice["content"] += f"- \"The Hidden Challenges of {selected_profile['interests'][0]} That Nobody Talks About\"\n"
                            advice["content"] += "- \"Discover What's Possible: Reimagining Your Approach to " + (category if category != "All Categories" else selected_profile["interests"][0]) + "\"\n"
                        
                        elif selected_profile["buying_stage"] == "Consideration":
                            advice["content"] += "Focus on solution comparison and value demonstration. Help this consumer evaluate options and see your unique value.\n\n"
                            advice["content"] += "Suggested headlines:\n"
                            advice["content"] += f"- \"Why Busy {selected_profile['occupation']}s Choose Our {category if category != 'All Categories' else 'Products'}\"\n"
                            advice["content"] += "- \"5 Ways Our Approach Stands Apart in " + (category if category != "All Categories" else selected_profile["interests"][0]) + "\"\n"
                            advice["content"] += f"- \"How We Address the Top 3 {', '.join(selected_profile['pain_points'][:1])} Challenges\"\n"
                        
                        else:  # Decision
                            advice["content"] += "Focus on risk reduction and purchase facilitation. Make the final decision easy and low-risk.\n\n"
                            advice["content"] += "Suggested headlines:\n"
                            advice["content"] += "- \"Join Thousands Who've Transformed Their " + (category if category != "All Categories" else selected_profile["interests"][0]) + " Experience\"\n"
                            advice["content"] += "- \"Our 30-Day Satisfaction Guarantee Means Zero Risk\"\n"
                            advice["content"] += f"- \"Special Offer for {selected_profile['location']} {selected_profile['occupation']}s: Start Today\"\n"
                        
                        # Add channel recommendations
                        advice["content"] += "\nRecommended channels:\n"
                        if selected_profile["age"] < 30:
                            advice["content"] += "- Social media (Instagram, TikTok)\n- Mobile-first content\n- Influencer partnerships\n"
                        elif selected_profile["age"] < 45:
                            advice["content"] += "- LinkedIn\n- Email newsletters\n- Podcast sponsorships\n"
                        else:
                            advice["content"] += "- Email campaigns\n- Industry publications\n- Facebook\n"
                    
                    elif advice_type == "Pricing Strategy":
                        # Generate pricing advice
                        advice = {
                            "type": advice_type,
                            "date": "Today",
                            "content": f"Pricing strategy recommendations for {selected_profile['name']}:\n\n"
                        }
                        
                        # Check for price sensitivity
                        if "Price sensitivity" in selected_profile["pain_points"]:
                            advice["content"] += "This consumer shows price sensitivity. Consider these strategies:\n\n"
                            advice["content"] += "1. Value-tier offerings with essential features only\n"
                            advice["content"] += "2. Installment payment options\n"
                            advice["content"] += "3. Entry-level products with upgrade paths\n"
                            advice["content"] += "4. Loyalty programs that reward repeat purchases\n"
                            advice["content"] += "5. Bundle discounts for complementary products\n\n"
                            
                            advice["content"] += "Avoid premium pricing or luxury positioning as this may create immediate barriers."
                        else:
                            advice["content"] += "This consumer prioritizes value over lowest price. Consider these strategies:\n\n"
                            advice["content"] += "1. Good-better-best tiering with clear value steps\n"
                            advice["content"] += "2. Premium options with additional services included\n"
                            advice["content"] += "3. Subscription models with exclusive benefits\n"
                            advice["content"] += "4. Value-based pricing highlighting ROI\n"
                            advice["content"] += "5. Early adopter or VIP pricing tiers\n\n"
                            
                            advice["content"] += "Emphasize the quality/price relationship rather than focusing on discount messaging."
                    
                    # Add the advice to history
                    st.session_state.advice_history.append(advice)
                    
                # Display the advice
                st.markdown(f"""
                <div class="consumer-card">
                    <h3>AI Recommendation</h3>
                    <p style="white-space: pre-line">{advice["content"]}</p>
                </div>
                """, unsafe_allow_html=True)
    
    # Show advice history
    if st.session_state.advice_history:
        st.subheader("Previous Advice")
        for advice in reversed(st.session_state.advice_history[:-1][:3]):  # Show last 3 excluding the most recent
            st.markdown(f"""
            <div class="consumer-card" style="opacity: 0.8">
                <h4>{advice["type"]} ({advice["date"]})</h4>
                <p style="white-space: pre-line">{advice["content"][:150]}...</p>
            </div>
            """, unsafe_allow_html=True)

elif page == "📊 Insights & Analytics":
    st.title("Consumer Insights Analytics")
    
    # Create some sample data for analytics
    profile_data = pd.DataFrame([
        {
            "name": p["name"],
            "age": p["age"],
            "location": p["location"],
            "buying_stage": p["buying_stage"],
            "interests_count": len(p["interests"]),
            "pain_points_count": len(p["pain_points"])
        } for p in st.session_state.consumer_profiles
    ])
    
    # Display analytics tabs
    tab1, tab2, tab3 = st.tabs(["Demographics", "Interests & Pain Points", "Buying Stages"])
    
    with tab1:
        st.subheader("Consumer Demographics")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Age distribution
            st.markdown("<div class='consumer-card'>", unsafe_allow_html=True)
            st.write("Age Distribution")
            
            fig, ax = plt.subplots(figsize=(8, 5))
            sns.histplot(profile_data["age"], bins=5, kde=True, ax=ax)
            st.pyplot(fig)
            st.markdown("</div>", unsafe_allow_html=True)
        
        with col2:
            # Location distribution
            st.markdown("<div class='consumer-card'>", unsafe_allow_html=True)
            st.write("Location Distribution")
            
            location_counts = profile_data["location"].value_counts()
            fig, ax = plt.subplots(figsize=(8, 5))
            plt.pie(location_counts, labels=location_counts.index, autopct='%1.1f%%', startangle=90)
            plt.axis('equal')
            st.pyplot(fig)
            st.markdown("</div>", unsafe_allow_html=True)
    
    with tab2:
        st.subheader("Consumer Interests & Pain Points")
        
        # Gather all interests and pain points
        all_interests = []
        all_pain_points = []
        
        for profile in st.session_state.consumer_profiles:
            all_interests.extend(profile["interests"])
            all_pain_points.extend(profile["pain_points"])
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Interests visualization
            st.markdown("<div class='consumer-card'>", unsafe_allow_html=True)
            st.write("Top Interests")
            
            interest_counts = pd.Series(all_interests).value_counts()
            fig, ax = plt.subplots(figsize=(8, 5))
            sns.barplot(x=interest_counts.values, y=interest_counts.index, ax=ax)
            plt.tight_layout()
            st.pyplot(fig)
            st.markdown("</div>", unsafe_allow_html=True)
        
        with col2:
            # Pain points visualization
            st.markdown("<div class='consumer-card'>", unsafe_allow_html=True)
            st.write("Top Pain Points")
            
            pain_point_counts = pd.Series(all_pain_points).value_counts()
            fig, ax = plt.subplots(figsize=(8, 5))
            sns.barplot(x=pain_point_counts.values, y=pain_point_counts.index, ax=ax)
            plt.tight_layout()
            st.pyplot(fig)
            st.markdown("</div>", unsafe_allow_html=True)
    
    with tab3:
        st.subheader("Consumer Buying Stages")
        
        # Buying stages visualization
        st.markdown("<div class='consumer-card'>", unsafe_allow_html=True)
        st.write("Distribution of Buying Stages")
        
        buying_stage_counts = profile_data["buying_stage"].value_counts()
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.barplot(x=buying_stage_counts.index, y=buying_stage_counts.values, ax=ax)
        plt.ylabel("Number of Consumers")
        plt.xlabel("Buying Stage")
        st.pyplot(fig)
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Funnel visualization
        st.markdown("<div class='consumer-card'>", unsafe_allow_html=True)
        st.write("Consumer Journey Funnel")
        
        stages = ["Awareness", "Consideration", "Decision"]
        stage_counts = [sum(profile_data["buying_stage"] == stage) for stage in stages]
        
        fig, ax = plt.subplots(figsize=(10, 6))
        plt.bar(stages, stage_counts, width=0.6)
        
        # Add conversion rate arrows
        if stage_counts[0] > 0 and stage_counts[1] > 0:
            awareness_to_consideration = f"{(stage_counts[1] / stage_counts[0]) * 100:.1f}%"
            plt.annotate(f"→ {awareness_to_consideration}", 
                        xy=(0.5, min(stage_counts[0], stage_counts[1]) + 0.1),
                        xytext=(0.5, min(stage_counts[0], stage_counts[1]) + 0.1),
                        arrowprops=dict(arrowstyle="->"))
        
        if stage_counts[1] > 0 and stage_counts[2] > 0:
            consideration_to_decision = f"{(stage_counts[2] / stage_counts[1]) * 100:.1f}%"
            plt.annotate(f"→ {consideration_to_decision}", 
                        xy=(1.5, min(stage_counts[1], stage_counts[2]) + 0.1),
                        xytext=(1.5, min(stage_counts[1], stage_counts[2]) + 0.1),
                        arrowprops=dict(arrowstyle="->"))
        
        plt.ylabel("Number of Consumers")
        plt.title("Consumer Journey Stage Conversion")
        st.pyplot(fig)
        
        st.markdown("</div>", unsafe_allow_html=True)

elif page == "⚙️ Settings":
    st.title("Application Settings")
    
    with st.expander("Consumer Profile Settings"):
        st.checkbox("Allow custom attributes for consumer profiles", value=True)
        st.number_input("Maximum number of consumer profiles", min_value=5, max_value=100, value=20)
        st.checkbox("Enable consumer journey tracking", value=True)
    
    with st.expander("AI Advisor Settings"):
        st.slider("Creativity level for recommendations", min_value=0, max_value=10, value=7)
        st.multiselect("Enabled advice types", 
                      ["Product Recommendations", "Marketing Messaging", "Pricing Strategy", "Customer Experience", "Feature Prioritization"],
                      default=["Product Recommendations", "Marketing Messaging", "Pricing Strategy"])
        st.checkbox("Include competitive analysis in recommendations", value=False)
    
    with st.expander("Data Management"):
        st.checkbox("Store historical advice records", value=True)
        st.number_input("Days to retain advice history", min_value=30, max_value=365, value=90)
        st.button("Export All Consumer Profiles (CSV)")
        st.button("Import Consumer Profiles")
    
    with st.expander("Advanced Settings"):
        st.checkbox("Enable debug mode", value=False)
        st.checkbox("Use experimental features", value=False)
        api_key = st.text_input("API Key (if connecting to external services)", type="password")
        st.button("Test API Connection")

# App footer
st.markdown("""
<div style='text-align: center; margin-top: 30px; opacity: 0.7;'>
    <p>Consumer Insights AI Demo | Created with Streamlit</p>
</div>
""", unsafe_allow_html=True)

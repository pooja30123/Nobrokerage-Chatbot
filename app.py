import streamlit as st
import pandas as pd
from backend.data_processor import load_master_data
from backend.query_parser import QueryParser
from backend.search_engine import PropertySearch
from backend.summarizer import SummaryGenerator

st.set_page_config(
    page_title="NoBrokerage Property Search",
    page_icon="🏠",
    layout="wide"
)

@st.cache_data
def load_data():
    return load_master_data()

@st.cache_resource
def get_components():
    df = load_data()
    parser = QueryParser()
    search_engine = PropertySearch(df)
    summarizer = SummaryGenerator()
    return df, parser, search_engine, summarizer

df, parser, search_engine, summarizer = get_components()

with st.sidebar:
    st.header("📊 Dataset Stats")
    st.metric("Total Properties", len(df))
    st.metric("Unique Locations", df['landmark'].nunique())
    min_price = df['price_crore'].min()
    max_price = df['price_crore'].max()
    st.metric("Price Range", f"₹{min_price:.2f} - ₹{max_price:.2f} Cr")
    st.markdown("---")
    st.markdown("### 💡 Example Queries")
    st.code("2BHK under 1 crore", language="text")
    st.code("1BHK in Chembur", language="text")
    st.code("3BHK ready to move", language="text")
    st.code("Flat near Lodha Xperia Mall", language="text")

st.title("🏠 NoBrokerage AI Property Search")
st.markdown("Find your dream home with intelligent search powered by AI")
st.markdown("---")

if 'messages' not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message['role']):
        st.markdown(message['content'])
        if 'properties' in message and message['properties']:
            for i, prop in enumerate(message['properties'], 1):
                with st.container():
                    st.markdown(f"### {i}. {prop['name']}")
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Price", prop['price'])
                    with col2:
                        st.metric("Type", prop['type'])
                    with col3:
                        st.metric("Area", prop['carpet_area'])
                    st.write(f"📍 **Landmark:** {prop['location']}")
                    st.write(f"🏠 **Full Address:** {prop['full_address']}")
                    st.write(f"🏗️ **Status:** {prop['status']}")
                    if prop.get('bathrooms'):
                        st.write(f"🚿 **Bathrooms:** {prop['bathrooms']}")
                    st.markdown("---")

if prompt := st.chat_input("Type your property requirement here..."):
    st.session_state.messages.append({'role': 'user', 'content': prompt})
    with st.chat_message('user'):
        st.markdown(prompt)
    
    filters = parser.parse(prompt)
    
    if 'invalid_query' in filters:
        with st.chat_message('assistant'):
            st.markdown("I can help you find properties, but I can't answer general questions. Please ask about:")
            st.markdown("- Types of flats (1BHK, 2BHK, etc.)")
            st.markdown("- Budget (under X lakh/crore)")
            st.markdown("- Locations (in Mumbai, Pune, etc.)")
            st.markdown("- Status (ready to move, under construction)")
            st.session_state.messages.append({
                'role': 'assistant',
                'content': "I can help you find properties, but I can't answer general questions. Please ask about property types, budget, locations, or possession status."
            })
    
    elif not filters:
        with st.chat_message('assistant'):
            st.warning("⚠️ I couldn't find any property filters in your query. Please specify:")
            st.markdown("- BHK type (1BHK, 2BHK, etc.)")
            st.markdown("- Budget (under X lakh/crore)")
            st.markdown("- Location (in Mumbai, Pune, etc.)")
            st.markdown("- Status (ready to move, under construction)")
            st.session_state.messages.append({
                'role': 'assistant',
                'content': "I couldn't find any property filters in your query. Please specify BHK type, budget, location, or possession status."
            })
    
    else:
        with st.chat_message('assistant'):
            with st.spinner('🔍 Searching properties...'):
                filter_chips = []
                if 'bhk' in filters:
                    filter_chips.append(f"🏠 {filters['bhk']}BHK")
                if 'max_price_crore' in filters:
                    filter_chips.append(f"💰 Under ₹{filters['max_price_crore']} Cr")
                if 'status' in filters:
                    filter_chips.append(f"🏗️ {filters['status'].replace('_', ' ').title()}")
                if 'location' in filters:
                    filter_chips.append(f"📍 {filters['location']}")
                st.info("Applied filters: " + " | ".join(filter_chips))
                
                results = search_engine.search(filters)
                stats = search_engine.get_stats(results)
                summary = summarizer.generate_summary(prompt, results, stats)
                st.markdown(summary)
                
                properties = []
                if len(results) > 0:
                    st.markdown("---")
                    st.markdown(f"### 🏘️ Top {min(8, len(results))} Properties")
                    for idx, row in results.head(8).iterrows():
                        price_display = f"₹{row['price_crore']:.2f} Cr" if row['price_crore'] >= 1 else f"₹{row['price_lakh']:.2f} L"
                        prop = {
                            'name': row['projectName'],
                            'type': row['type'],
                            'price': price_display,
                            'location': row['landmark'] if pd.notna(row['landmark']) else 'Not specified',
                            'full_address': row['fullAddress'] if pd.notna(row['fullAddress']) else 'Not specified',
                            'status': 'Ready to Move' if row['is_ready'] else 'Under Construction',
                            'carpet_area': f"{row['carpetArea']:.0f} sq.ft" if pd.notna(row['carpetArea']) else 'N/A',
                            'bathrooms': f"{int(row['bathrooms'])}" if pd.notna(row['bathrooms']) else None
                        }
                        properties.append(prop)
                        with st.container():
                            st.markdown(f"### {len(properties)}. {prop['name']}")
                            col1, col2, col3 = st.columns(3)
                            with col1:
                                st.metric("Price", prop['price'])
                            with col2:
                                st.metric("Type", prop['type'])
                            with col3:
                                st.metric("Area", prop['carpet_area'])
                            st.write(f"📍 **Landmark:** {prop['location']}")
                            st.write(f"🏠 **Full Address:** {prop['full_address']}")
                            st.write(f"🏗️ **Status:** {prop['status']}")
                            if prop['bathrooms']:
                                st.write(f"🚿 **Bathrooms:** {prop['bathrooms']}")
                            st.markdown("---")
                
                st.session_state.messages.append({
                    'role': 'assistant',
                    'content': summary,
                    'properties': properties if properties else None
                })

st.markdown("---")
st.caption("🤖 Powered by Google Gemini AI | Built with Streamlit")

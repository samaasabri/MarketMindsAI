import streamlit as st
import datetime
from requests.exceptions import ReadTimeout
from agents.industry_agents import IndustryReportOrchestrator
from utils.chart_generator import generate_pie_chart, generate_bar_chart, generate_line_chart

# Page Configuration
st.set_page_config(
    page_title="Industry Intelligence Generator",
    layout="wide",
    page_icon="📊"
)

# Sidebar Content
with st.sidebar:
    st.title("📘 How to Use")
    st.markdown("""
    1. Enter a high-level query like:
       - _"Generate a strategy intelligence report for the AI market."_
       - _"Report on competitors in the electric vehicle industry."_
    2. Click **Generate Report**.
    3. Review the structured analysis below.
    """)
    st.markdown("---")
    st.markdown("⚡ Powered by **LangChain + Mistral**")
    st.markdown("🛠 Built by Samaa Sabry")

# Main Content
st.markdown("# 📊 Industry Intelligence Report Generator")
st.markdown("This tool autonomously researches, analyzes, and creates a strategic report for your chosen market or company.")

query = st.text_input("🔍 Enter your industry query", placeholder="e.g. Generate a strategy intelligence report for the electric vehicle market and its key players")

if st.button("🚀 Generate Report") and query:
    if not query.strip():  # Check if the input query is empty or only contains whitespace
        st.warning("⚠️ Please enter a valid query before generating the report.")
    else:
        with st.spinner("Running research agents, gathering insights..."):
            try:
                orchestrator = IndustryReportOrchestrator()

                # Step 1: Research
                st.markdown("## 🧠 Step 1: Researching the Market...")
                research_output = orchestrator.research_agent.run(query)
                
                # Handle empty or invalid research output
                if not research_output:
                    st.warning("⚠️ No research data was returned. Please refine your query or try again.")
                    

                st.success("Research complete.")
                st.expander("🔍 Research Summary").markdown(research_output)

                # Step 2: Analysis
                st.markdown("## 📈 Step 2: Market Analysis...")
                analysis_output = orchestrator.analysis_agent.run({"research_data": research_output})

                # Handle analysis step failure
                if not analysis_output:
                    st.warning("⚠️ No analysis data returned. Please check the research data.")
                    

                st.success("Analysis complete.")
                st.expander("📊 Competitor & Market Trends").markdown(analysis_output)

                # Step 3: Visualization
                st.markdown("## 📊 Step 3: Visual Insights...")
                visualization_output = orchestrator.visualization_agent.run(research_output)
                st.success("Visualization completed.")

                with st.expander("### 📊 Visualization"):
                    try:
                        chart_data = visualization_output

                        if "market_share" in chart_data:
                            st.subheader("🥧 Market Share")
                            fig = generate_pie_chart(chart_data["market_share"], title="Market Share")
                            st.pyplot(fig)

                        if "market_growth" in chart_data:
                            st.subheader("📈 Market Growth")
                            fig = generate_line_chart(chart_data["market_growth"], title="Market Growth Over Time", xlabel="Year", ylabel="Growth %")
                            st.pyplot(fig)

                        if "competitor_comparison" in chart_data:
                            st.subheader("🏁 Competitor Comparison")
                            fig = generate_bar_chart(chart_data["competitor_comparison"], title="Competitor Performance", xlabel="Company", ylabel="Score")
                            st.pyplot(fig)

                    except Exception as e:
                        st.warning(f"⚠️ Error parsing visualization JSON: {e}")
                        st.expander("Raw Visualization Output").code(visualization_output)

                # Step 4: Strategy
                st.markdown("## 🎯 Step 4: Strategic Recommendations...")
                strategy_output = orchestrator.strategy_agent.run({"analysis_data": analysis_output})

                # Handle strategy step failure
                if not strategy_output:
                    st.warning("⚠️ No strategic recommendations returned.")
                    

                st.success("Strategy generated.")
                st.expander("🎯 Strategic Recommendations").markdown(strategy_output)

                # Final Report
                st.markdown("## 📝 Final Report")
                timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                filename = f"industry_report_{timestamp}.md"

                try:
                    final_report = orchestrator.writer_agent.run({
                        "research_data": research_output,
                        "analysis_data": analysis_output,
                        "strategy_data": strategy_output
                    })
                except Exception as e:
                    st.error(f"⚠️ Error while generating the final report: {e}")

                st.download_button(
                    label="📥 Download Report",
                    data=final_report,
                    file_name=filename,
                    mime="text/markdown"
                )

                st.success("✅ Full Report Generated")
                st.markdown(final_report, unsafe_allow_html=True)

            except ReadTimeout:
                st.error("⚠️ The request timed out. Please try again later.")
            except ConnectionError:
                st.error("⚠️ Network error. Please check your internet connection and try again.")
            except Exception as e:
                st.error(f"⚠️ An error occurred while generating the report: {e}")
else:
    st.info("Enter a query and click **Generate Report** to begin.")

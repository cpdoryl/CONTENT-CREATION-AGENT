"""Streamlit dashboard for content generation, review, and finalization"""

import streamlit as st
import json
from pathlib import Path
from datetime import datetime
import pandas as pd
from src.agents.research_agent import ResearchAgent
from src.agents.script_agent import ScriptAgent
from src.agents.visual_agent import VisualAgent
from src.agents.voice_agent import VoiceAgent
from src.core.models import ContentTopic, ContentPackage
from src.core.config import settings

st.set_page_config(
    page_title="Content Generation Studio",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Session State ────────────────────────────────────────────────────────────
if "topics" not in st.session_state:
    st.session_state.topics = []
if "packages" not in st.session_state:
    st.session_state.packages = {}
if "current_topic" not in st.session_state:
    st.session_state.current_topic = None
if "edits" not in st.session_state:
    st.session_state.edits = {}

# ── Sidebar Navigation ───────────────────────────────────────────────────────
st.sidebar.title("📺 Content Studio")
page = st.sidebar.radio(
    "Navigation",
    ["⚡ Auto Pipeline", "🚀 Generate", "📝 Review & Edit", "⬇️ Download", "📊 Dashboard"]
)

st.sidebar.divider()
st.sidebar.markdown("### Settings")
niche = st.sidebar.text_input("Niche", value=settings.NICHE)
audience = st.sidebar.text_input("Target Audience", value=settings.TARGET_AUDIENCE)

# Pipeline state
if "pipeline_stage" not in st.session_state:
    st.session_state.pipeline_stage = 0
if "pipeline_topics" not in st.session_state:
    st.session_state.pipeline_topics = []
if "pipeline_packages" not in st.session_state:
    st.session_state.pipeline_packages = []
if "pipeline_num_pieces" not in st.session_state:
    st.session_state.pipeline_num_pieces = 5
if "pipeline_approved_stages" not in st.session_state:
    st.session_state.pipeline_approved_stages = {}


# ── PAGE 0: AUTOMATED PIPELINE ──────────────────────────────────────────────
if page == "⚡ Auto Pipeline":
    st.title("⚡ Automated Content Pipeline")

    # Progress indicator
    stages = ["Research", "Review Topics", "Generate Content", "Review Content", "Final Export"]
    st.progress(
        (st.session_state.pipeline_stage) / (len(stages) - 1) if st.session_state.pipeline_stage > 0 else 0,
        text=f"Stage {st.session_state.pipeline_stage + 1}/{len(stages)}"
    )

    st.divider()

    # ── STAGE 0: RESEARCH TRENDS ──
    if st.session_state.pipeline_stage == 0:
        st.subheader("📊 Stage 1: Research Trending Topics")
        st.markdown("Searching for trending topics in your niche...")

        if st.button("🚀 Start Research", use_container_width=True):
            with st.spinner("🔎 Researching trends..."):
                try:
                    agent = ResearchAgent()
                    st.session_state.pipeline_topics = agent.research_trends(niche=niche, audience=audience)
                    st.session_state.pipeline_stage = 1
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ Research failed: {e}")

    # ── STAGE 1: REVIEW & SELECT TOPICS ──
    elif st.session_state.pipeline_stage == 1:
        st.subheader("📋 Stage 2: Review & Select Topics")
        st.markdown(f"Found **{len(st.session_state.pipeline_topics)}** trending topics")

        # Show topics
        for i, topic in enumerate(st.session_state.pipeline_topics):
            with st.expander(f"#{topic.priority_score} {topic.topic}", expanded=(i==0)):
                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"**Hook Angle:** {topic.hook_angle}")
                    st.write(f"**Format:** {topic.recommended_format}")
                with col2:
                    st.write(f"**Pain Point:** {topic.pain_point}")
                    st.write(f"**Why Trending:** {topic.why_trending}")

        # Select how many pieces to generate
        col1, col2 = st.columns(2)
        with col1:
            num_pieces = st.slider(
                "How many pieces to generate?",
                min_value=1,
                max_value=min(5, len(st.session_state.pipeline_topics)),
                value=st.session_state.pipeline_num_pieces
            )
            st.session_state.pipeline_num_pieces = num_pieces

        col1, col2 = st.columns(2)
        with col1:
            if st.button("← Back", use_container_width=True):
                st.session_state.pipeline_stage = 0
                st.rerun()
        with col2:
            if st.button("✅ Approve & Continue →", use_container_width=True):
                st.session_state.pipeline_approved_stages[1] = True
                st.session_state.pipeline_stage = 2
                st.rerun()

    # ── STAGE 2: GENERATE CONTENT ──
    elif st.session_state.pipeline_stage == 2:
        st.subheader("✍️ Stage 3: Generating Content Packages")

        progress_bar = st.progress(0)
        status_text = st.empty()

        selected_topics = st.session_state.pipeline_topics[:st.session_state.pipeline_num_pieces]
        st.session_state.pipeline_packages = []

        script_agent = ScriptAgent()

        for idx, topic in enumerate(selected_topics):
            status_text.text(f"Generating content for: {topic.topic} ({idx+1}/{len(selected_topics)})")
            progress_bar.progress((idx + 1) / len(selected_topics))

            try:
                package = script_agent.create_content_package(topic)
                st.session_state.pipeline_packages.append({
                    "topic": topic,
                    "package": package,
                    "approved": True
                })
            except Exception as e:
                st.error(f"Failed for {topic.topic}: {str(e)[:100]}")

        status_text.text("✅ All content generated!")
        st.success(f"Generated {len(st.session_state.pipeline_packages)} content packages!")

        col1, col2 = st.columns(2)
        with col1:
            if st.button("← Back", use_container_width=True):
                st.session_state.pipeline_stage = 1
                st.rerun()
        with col2:
            if st.button("✅ Review & Approve →", use_container_width=True):
                st.session_state.pipeline_stage = 3
                st.rerun()

    # ── STAGE 3: REVIEW CONTENT ──
    elif st.session_state.pipeline_stage == 3:
        st.subheader("📝 Stage 4: Review & Approve Content")
        st.info("✅ All items are approved by default. Uncheck to exclude from export.")

        # Initialize all as approved if not already set
        for idx, item in enumerate(st.session_state.pipeline_packages):
            if "approved" not in item or item["approved"] is None:
                st.session_state.pipeline_packages[idx]["approved"] = True

        # Show approval status summary
        approved_count = sum(1 for item in st.session_state.pipeline_packages if item["approved"])
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Items", len(st.session_state.pipeline_packages))
        with col2:
            st.metric("Approved ✅", approved_count)
        with col3:
            st.metric("Excluded ❌", len(st.session_state.pipeline_packages) - approved_count)

        st.divider()

        # Show each item with toggle
        for idx, item in enumerate(st.session_state.pipeline_packages):
            topic = item["topic"]
            package = item["package"]
            is_approved = item.get("approved", True)

            # Color-coded header
            status_icon = "✅" if is_approved else "❌"
            with st.expander(f"{status_icon} {topic.topic}", expanded=(idx==0)):
                col1, col2 = st.columns(2)

                with col1:
                    st.markdown("**Reel Script (Hook)**")
                    st.info(package.reel_script.hook)
                    st.markdown(f"**Word Count:** {package.reel_script.word_count}")

                with col2:
                    st.markdown("**Full Script**")
                    st.text_area(
                        f"Script {idx}",
                        value=package.reel_script.full_script,
                        height=120,
                        disabled=True,
                        key=f"script_{idx}"
                    )

                st.divider()

                col1, col2 = st.columns(2)
                with col1:
                    st.markdown("**Carousel (6 Slides)**")
                    for i, slide in enumerate(package.carousel_slides, 1):
                        st.write(f"{i}. {slide.headline}")

                with col2:
                    st.markdown("**Caption**")
                    st.text_area(
                        f"Caption {idx}",
                        value=package.caption[:150] + "...",
                        height=80,
                        disabled=True,
                        key=f"caption_{idx}"
                    )

                st.divider()
                st.markdown(f"**Hashtags:** {len(package.hashtags)} tags")

                col1, col2 = st.columns([3, 1])
                with col1:
                    st.markdown("**Approval Status**")
                with col2:
                    # Toggle button for approval
                    if st.button(
                        f"{'✅ APPROVED' if is_approved else '❌ EXCLUDED'}",
                        key=f"toggle_approve_{idx}",
                        use_container_width=True
                    ):
                        st.session_state.pipeline_packages[idx]["approved"] = not is_approved
                        st.rerun()

        st.divider()

        col1, col2 = st.columns(2)
        with col1:
            if st.button("← Back", use_container_width=True):
                st.session_state.pipeline_stage = 2
                st.rerun()
        with col2:
            approved_count = sum(1 for item in st.session_state.pipeline_packages if item["approved"])
            if approved_count > 0:
                if st.button(f"✅ Export {approved_count} Items →", use_container_width=True):
                    st.session_state.pipeline_approved_stages[3] = True
                    st.session_state.pipeline_stage = 4
                    st.rerun()
            else:
                st.warning("⚠️ Please approve at least 1 item to export")

    # ── STAGE 4: FINAL EXPORT ──
    elif st.session_state.pipeline_stage == 4:
        st.subheader("📦 Stage 5: Export & Download")

        approved_items = [item for item in st.session_state.pipeline_packages if item["approved"]]

        if not approved_items:
            st.warning("No approved content to export")
        else:
            st.success(f"✅ {len(approved_items)} content pieces ready to export!")

            # Create summary table
            summary_data = []
            for item in approved_items:
                topic = item["topic"]
                package = item["package"]
                summary_data.append({
                    "Topic": topic.topic,
                    "Hook": package.reel_script.hook[:40] + "...",
                    "Words": package.reel_script.word_count,
                    "Slides": len(package.carousel_slides),
                    "Hashtags": len(package.hashtags)
                })

            st.dataframe(pd.DataFrame(summary_data), use_container_width=True, hide_index=True)

            st.divider()

            # Export options
            col1, col2, col3 = st.columns(3)

            with col1:
                st.markdown("### 📥 Download Individual Items")
                selected_topic = st.selectbox(
                    "Select content to download:",
                    [item["topic"].topic for item in approved_items]
                )

                selected_item = next(item for item in approved_items if item["topic"].topic == selected_topic)
                package = selected_item["package"]

                st.download_button(
                    "📄 Script.txt",
                    data=package.reel_script.full_script,
                    file_name=f"{selected_topic}_script.txt"
                )
                st.download_button(
                    "📝 Caption.txt",
                    data=package.caption,
                    file_name=f"{selected_topic}_caption.txt"
                )
                st.download_button(
                    "#️⃣ Hashtags.txt",
                    data="\n".join(package.hashtags),
                    file_name=f"{selected_topic}_hashtags.txt"
                )

            with col2:
                st.markdown("### 📦 Export All as JSON")
                all_data = {
                    "generated_at": datetime.now().isoformat(),
                    "niche": niche,
                    "audience": audience,
                    "pieces": [
                        {
                            "topic": item["topic"].topic,
                            "script": item["package"].reel_script.full_script,
                            "caption": item["package"].caption,
                            "hashtags": item["package"].hashtags,
                            "carousel_slides": [
                                {"headline": s.headline, "body": s.body}
                                for s in item["package"].carousel_slides
                            ]
                        }
                        for item in approved_items
                    ]
                }
                st.download_button(
                    "📦 Complete.json",
                    data=json.dumps(all_data, indent=2),
                    file_name=f"content_package_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
                )

            with col3:
                st.markdown("### 🔄 Next Steps")
                st.markdown("""
                1. ✅ Content generated
                2. ✅ Downloaded files
                3. 📱 Post to Instagram
                4. 📊 Track engagement
                """)

            st.divider()

            col1, col2 = st.columns(2)
            with col1:
                if st.button("← Back to Review", use_container_width=True):
                    st.session_state.pipeline_stage = 3
                    st.rerun()
            with col2:
                if st.button("🔄 Start New Pipeline", use_container_width=True):
                    st.session_state.pipeline_stage = 0
                    st.session_state.pipeline_topics = []
                    st.session_state.pipeline_packages = []
                    st.rerun()


# ── PAGE 1: GENERATE ─────────────────────────────────────────────────────────
elif page == "🚀 Generate":
    st.title("🚀 Content Generation")

    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown("""
        ### Generate New Content Ideas
        Find trending topics and create complete content pieces with scripts, visuals, and voiceovers.
        """)

    with col2:
        st.info(f"📊 Niche: {niche}")

    st.divider()

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("1️⃣ Research Trends")
        if st.button("🔍 Find Trending Topics", key="research_btn", use_container_width=True):
            with st.spinner(f"🔎 Researching trends for: {niche}"):
                try:
                    agent = ResearchAgent()
                    # Pass custom niche and audience to research
                    st.session_state.topics = agent.research_trends(niche=niche, audience=audience)
                    st.session_state.current_topic = None  # Reset current selection
                    st.success(f"✅ Found {len(st.session_state.topics)} trending topics!")
                except Exception as e:
                    st.error(f"❌ Research failed: {e}")

    with col2:
        st.subheader("Topics Found")
        if st.session_state.topics:
            st.metric("Total Topics", len(st.session_state.topics))

    st.divider()

    if st.session_state.topics:
        st.subheader("2️⃣ Select Topic & Create Package")

        topic_names = [f"#{t.priority_score} {t.topic}" for t in st.session_state.topics]
        # Use number of topics as key to force refresh when topics change
        selected_idx = st.selectbox(
            "Choose a topic:",
            range(len(topic_names)),
            format_func=lambda i: topic_names[i],
            key=f"topic_select_{len(st.session_state.topics)}"
        )

        if selected_idx is not None:
            topic = st.session_state.topics[selected_idx]
            st.session_state.current_topic = topic

            col1, col2, col3 = st.columns(3)
            with col1:
                st.write(f"**Topic:** {topic.topic}")
            with col2:
                st.write(f"**Angle:** {topic.hook_angle}")
            with col3:
                st.write(f"**Format:** {topic.recommended_format}")

            if st.button("✨ Generate Full Content Package", use_container_width=True, key="generate_package"):
                with st.spinner("⏳ Creating scripts, visuals, voiceovers..."):
                    try:
                        script_agent = ScriptAgent()
                        package = script_agent.create_content_package(topic)
                        st.session_state.packages[topic.topic] = package
                        st.session_state.edits[topic.topic] = {
                            "hook": package.reel_script.hook,
                            "full_script": package.reel_script.full_script,
                            "caption": package.caption,
                            "hashtags": package.hashtags,
                            "carousel_slides": [{"headline": s.headline, "body": s.body} for s in package.carousel_slides]
                        }
                        st.success("✅ Content package created!")
                        st.balloons()

                        # Display generated content immediately
                        st.divider()
                        st.subheader("📄 Generated Content Preview")

                        # Display script
                        with st.expander("📹 Reel Script", expanded=True):
                            st.markdown("**Hook (0-3 seconds):**")
                            st.info(package.reel_script.hook)
                            st.markdown("**Full Script (45 seconds):**")
                            st.text_area("Script content", value=package.reel_script.full_script, height=150, disabled=True, key="preview_script")
                            st.metric("Word Count", package.reel_script.word_count)

                        # Display carousel
                        with st.expander("📸 Carousel (6 Slides)", expanded=False):
                            for i, slide in enumerate(package.carousel_slides, 1):
                                st.markdown(f"**Slide {i}**")
                                st.write(f"**Headline:** {slide.headline}")
                                st.write(f"**Body:** {slide.body}")
                                st.divider()

                        # Display caption
                        with st.expander("📝 Instagram Caption", expanded=False):
                            st.text_area("Caption", value=package.caption, height=150, disabled=True, key="preview_caption")
                            st.info(f"Length: {len(package.caption)} characters")

                        # Display hashtags
                        with st.expander("#️⃣ Hashtags (30)", expanded=False):
                            hashtags_text = "\n".join(package.hashtags)
                            st.text_area("Hashtags", value=hashtags_text, height=200, disabled=True, key="preview_hashtags")
                            st.info(f"Total: {len(package.hashtags)} hashtags")

                        st.divider()
                        st.info("👉 Go to **📝 Review & Edit** tab to customize, or **⬇️ Download** to export all files!")

                    except Exception as e:
                        st.error(f"❌ Failed: {str(e)[:200]}")


# ── PAGE 2: REVIEW & EDIT ────────────────────────────────────────────────────
if page == "📝 Review & Edit":
    st.title("📝 Review & Edit Content")

    if not st.session_state.packages:
        st.warning("⚠️ No packages generated yet. Go to Generate tab first.")
    else:
        # Select package to review
        package_names = list(st.session_state.packages.keys())
        selected_package = st.selectbox("Select content piece:", package_names)

        if selected_package:
            package = st.session_state.packages[selected_package]
            edits = st.session_state.edits.get(selected_package, {})

            st.divider()

            # Tabs for different content types
            tab1, tab2, tab3, tab4, tab5 = st.tabs(["📹 Reel Script", "📸 Carousel", "📝 Caption", "#️⃣ Hashtags", "🎨 Visuals"])

            # ── TAB 1: REEL SCRIPT ──
            with tab1:
                st.subheader("Reel Script (45 seconds)")

                col1, col2 = st.columns([1, 1])

                with col1:
                    st.markdown("**Hook (0-3s)**")
                    hook = st.text_area(
                        "Opening line",
                        value=edits.get("hook", package.reel_script.hook),
                        height=60,
                        key="hook_edit"
                    )
                    edits["hook"] = hook

                with col2:
                    st.markdown("**Stats**")
                    st.metric("Word Count", len(package.reel_script.full_script.split()))
                    st.metric("Duration", "45s")

                st.markdown("**Full Script**")
                full_script = st.text_area(
                    "Complete reel script",
                    value=edits.get("full_script", package.reel_script.full_script),
                    height=200,
                    key="script_edit"
                )
                edits["full_script"] = full_script

                col1, col2, col3 = st.columns(3)
                with col1:
                    if st.button("🔊 Generate Voiceover", key="voice_gen"):
                        with st.spinner("🎙️ Generating voice..."):
                            try:
                                voice_agent = VoiceAgent()
                                output_path = Path("output") / f"{selected_package.replace(' ', '_')}.mp3"
                                voice_agent.generate_voiceover(full_script, output_path)
                                st.success("✅ Voiceover created!")
                                st.audio(str(output_path))
                            except Exception as e:
                                st.error(f"❌ Voice failed: {str(e)[:100]}")

            # ── TAB 2: CAROUSEL ──
            with tab2:
                st.subheader("6-Slide Carousel")

                carousel_slides = edits.get("carousel_slides",
                    [{"headline": s.headline, "body": s.body} for s in package.carousel_slides])

                for i, slide in enumerate(carousel_slides, 1):
                    with st.expander(f"Slide {i} - {slide.get('headline', '')[:30]}...", expanded=(i==1)):
                        col1, col2 = st.columns(2)

                        with col1:
                            headline = st.text_input(
                                f"Headline {i}",
                                value=slide.get("headline", ""),
                                key=f"slide_{i}_headline"
                            )
                            slide["headline"] = headline

                        with col2:
                            body = st.text_area(
                                f"Body {i}",
                                value=slide.get("body", ""),
                                height=80,
                                key=f"slide_{i}_body"
                            )
                            slide["body"] = body

                edits["carousel_slides"] = carousel_slides

            # ── TAB 3: CAPTION ──
            with tab3:
                st.subheader("Instagram Caption")

                caption = st.text_area(
                    "Caption text",
                    value=edits.get("caption", package.caption),
                    height=200,
                    key="caption_edit"
                )
                edits["caption"] = caption

                st.info(f"📊 Length: {len(caption)} characters (max 2200)")

            # ── TAB 4: HASHTAGS ──
            with tab4:
                st.subheader("Hashtags")

                hashtags = edits.get("hashtags", package.hashtags)
                hashtags_text = st.text_area(
                    "Hashtags (one per line)",
                    value="\n".join(hashtags),
                    height=300,
                    key="hashtags_edit"
                )
                edits["hashtags"] = [h.strip() for h in hashtags_text.split("\n") if h.strip()]

                st.info(f"📊 Count: {len(edits['hashtags'])} hashtags")

                # Show hashtag breakdown
                col1, col2, col3 = st.columns(3)
                with col1:
                    large = sum(1 for h in edits['hashtags'] if '#' in h)
                    st.metric("Total", len(edits['hashtags']))
                with col2:
                    st.metric("Ready to Copy", "✅")

            # ── TAB 5: VISUALS ──
            with tab5:
                st.subheader("Generated Visuals")

                col1, col2 = st.columns(2)

                with col1:
                    st.markdown("**Reel Background (9:16)**")
                    output_path = Path("output") / f"{selected_package.replace(' ', '_')}_reel.jpg"
                    if output_path.exists():
                        st.image(str(output_path), use_column_width=True)
                    else:
                        if st.button("🎨 Generate Reel Image", key="gen_reel_visual"):
                            with st.spinner("🖼️ Creating background..."):
                                try:
                                    visual_agent = VisualAgent()
                                    visual_agent.generate_reel_background(package, output_path)
                                    st.success("✅ Image created!")
                                    st.image(str(output_path), use_column_width=True)
                                except Exception as e:
                                    st.error(f"❌ Failed: {str(e)[:100]}")

                with col2:
                    st.markdown("**Post Image (1:1)**")
                    output_path = Path("output") / f"{selected_package.replace(' ', '_')}_post.jpg"
                    if output_path.exists():
                        st.image(str(output_path), use_column_width=True)
                    else:
                        if st.button("🎨 Generate Post Image", key="gen_post_visual"):
                            with st.spinner("🖼️ Creating image..."):
                                try:
                                    visual_agent = VisualAgent()
                                    visual_agent.generate_post_image(package, output_path)
                                    st.success("✅ Image created!")
                                    st.image(str(output_path), use_column_width=True)
                                except Exception as e:
                                    st.error(f"❌ Failed: {str(e)[:100]}")

            st.divider()

            # Save edits
            if st.button("💾 Save Edits", use_container_width=True, key="save_edits"):
                st.session_state.edits[selected_package] = edits
                st.success("✅ Edits saved to session")


# ── PAGE 3: DOWNLOAD ────────────────────────────────────────────────────────
if page == "⬇️ Download":
    st.title("⬇️ Download Content")

    if not st.session_state.packages:
        st.warning("⚠️ No packages generated yet.")
    else:
        package_names = list(st.session_state.packages.keys())
        selected_package = st.selectbox("Select content to download:", package_names)

        if selected_package:
            edits = st.session_state.edits.get(selected_package, {})

            st.divider()
            st.subheader(f"Content Package: {selected_package}")

            col1, col2 = st.columns(2)

            with col1:
                st.markdown("### 📄 Files Available")

                files_available = []
                output_dir = Path("output")

                # Check for script file
                script_file = output_dir / f"{selected_package.replace(' ', '_')}_script.txt"
                caption_file = output_dir / f"{selected_package.replace(' ', '_')}_caption.txt"
                hashtags_file = output_dir / f"{selected_package.replace(' ', '_')}_hashtags.txt"

                if st.button("📥 Download Script", key="dl_script"):
                    script_content = edits.get("full_script", "")
                    st.download_button(
                        label="Download Script.txt",
                        data=script_content,
                        file_name=f"{selected_package}_script.txt",
                        mime="text/plain"
                    )

                if st.button("📥 Download Caption", key="dl_caption"):
                    caption_content = edits.get("caption", "")
                    st.download_button(
                        label="Download Caption.txt",
                        data=caption_content,
                        file_name=f"{selected_package}_caption.txt",
                        mime="text/plain"
                    )

                if st.button("📥 Download Hashtags", key="dl_hashtags"):
                    hashtags_content = "\n".join(edits.get("hashtags", []))
                    st.download_button(
                        label="Download Hashtags.txt",
                        data=hashtags_content,
                        file_name=f"{selected_package}_hashtags.txt",
                        mime="text/plain"
                    )

                if st.button("📥 Download All as JSON", key="dl_json"):
                    json_content = json.dumps(edits, indent=2)
                    st.download_button(
                        label="Download Complete.json",
                        data=json_content,
                        file_name=f"{selected_package}_complete.json",
                        mime="application/json"
                    )

            with col2:
                st.markdown("### 🎨 Media Files")

                output_dir = Path("output")

                reel_path = output_dir / f"{selected_package.replace(' ', '_')}_reel.jpg"
                post_path = output_dir / f"{selected_package.replace(' ', '_')}_post.jpg"
                voice_path = output_dir / f"{selected_package.replace(' ', '_')}.mp3"

                if reel_path.exists():
                    with open(reel_path, "rb") as f:
                        st.download_button(
                            label="📥 Download Reel.jpg",
                            data=f.read(),
                            file_name=f"{selected_package}_reel.jpg",
                            mime="image/jpeg"
                        )

                if post_path.exists():
                    with open(post_path, "rb") as f:
                        st.download_button(
                            label="📥 Download Post.jpg",
                            data=f.read(),
                            file_name=f"{selected_package}_post.jpg",
                            mime="image/jpeg"
                        )

                if voice_path.exists():
                    with open(voice_path, "rb") as f:
                        st.download_button(
                            label="🎙️ Download Voiceover.mp3",
                            data=f.read(),
                            file_name=f"{selected_package}_voiceover.mp3",
                            mime="audio/mpeg"
                        )


# ── PAGE 4: DASHBOARD ────────────────────────────────────────────────────────
if page == "📊 Dashboard":
    st.title("📊 Content Dashboard")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Topics Generated", len(st.session_state.topics))

    with col2:
        st.metric("Content Packages", len(st.session_state.packages))

    with col3:
        st.metric("Edited Items", sum(len(v) for v in st.session_state.edits.values() if isinstance(v, dict)))

    st.divider()

    if st.session_state.packages:
        st.subheader("Generated Content")

        data = []
        for topic_name, package in st.session_state.packages.items():
            data.append({
                "Topic": topic_name,
                "Hook": package.reel_script.hook[:50] + "...",
                "Script Words": package.reel_script.word_count,
                "Slides": len(package.carousel_slides),
                "Hashtags": len(package.hashtags),
                "Status": "✅ Edited" if topic_name in st.session_state.edits else "⏳ Pending"
            })

        df = pd.DataFrame(data)
        st.dataframe(df, use_container_width=True, hide_index=True)

        st.divider()

        st.subheader("Quick Stats")
        col1, col2, col3 = st.columns(3)

        with col1:
            total_words = sum(p.reel_script.word_count for p in st.session_state.packages.values())
            st.metric("Total Script Words", total_words)

        with col2:
            total_hashtags = sum(len(p.hashtags) for p in st.session_state.packages.values())
            st.metric("Total Hashtags", total_hashtags)

        with col3:
            total_slides = sum(len(p.carousel_slides) for p in st.session_state.packages.values())
            st.metric("Carousel Slides", total_slides)

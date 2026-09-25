import streamlit as st
from html import escape

def subject_card(name, code, section, stats=None, footer_callback=None):
    stats_markup = ""
    if stats:
        stats_items = "".join(
            f'<div class="snap-subject-stat">'
            f'<span class="snap-subject-stat-icon">{escape(str(icon))}</span>'
            f'<span class="snap-subject-stat-copy">'
            f'<span class="snap-subject-stat-value">{escape(str(value))}</span>'
            f'<span class="snap-subject-stat-label">{escape(str(label))}</span>'
            f'</span>'
            f'</div>'
            for icon, label, value in stats
        )
        stats_markup = f'<div class="snap-subject-stats">{stats_items}</div>'

    with st.container():
        st.markdown(
            """
            <style>
                .snap-subject-card {
                    margin: 1rem 0 0.25rem;
                    padding: 1.25rem 1.35rem;
                    border: 1px solid rgba(88, 101, 242, 0.2);
                    border-left: 6px solid #EB459E;
                    border-radius: 1rem;
                    background: #FFFFFF;
                    box-shadow: 0 8px 22px rgba(32, 33, 58, 0.08);
                }

                .snap-subject-card-header {
                    display: flex;
                    align-items: flex-start;
                    justify-content: space-between;
                    gap: 1rem;
                }

                .snap-subject-card-title {
                    margin: 0;
                    color: #20213A;
                    font-size: 1.35rem;
                    font-weight: 700;
                    line-height: 1.2;
                }

                .snap-subject-card-section {
                    margin: 0.35rem 0 0;
                    color: #62647A;
                    font-size: 0.9rem;
                }

                .snap-subject-card-code {
                    flex: 0 0 auto;
                    padding: 0.35rem 0.65rem;
                    border-radius: 0.5rem;
                    background: #E0E3FF;
                    color: #5865F2;
                    font-size: 0.78rem;
                    font-weight: 700;
                    letter-spacing: 0.04em;
                }

                .snap-subject-stats {
                    display: flex;
                    flex-wrap: wrap;
                    gap: 1.25rem;
                    margin-top: 1.15rem;
                    padding-top: 1rem;
                    border-top: 1px solid #ECECFA;
                }

                .snap-subject-stat {
                    display: flex;
                    align-items: center;
                    gap: 0.55rem;
                }

                .snap-subject-stat-icon {
                    font-size: 1.2rem;
                }

                .snap-subject-stat-copy {
                    display: flex;
                    flex-direction: column;
                    line-height: 1.1;
                }

                .snap-subject-stat-value {
                    color: #20213A;
                    font-size: 1rem;
                    font-weight: 700;
                }

                .snap-subject-stat-label {
                    margin-top: 0.2rem;
                    color: #77798B;
                    font-size: 0.72rem;
                }

                @media (max-width: 600px) {
                    .snap-subject-card-header {
                        flex-direction: column;
                    }

                    .snap-subject-card-code {
                        align-self: flex-start;
                    }
                }
            </style>
            """,
            unsafe_allow_html=True,
        )
        card_html = (
            f'<article class="snap-subject-card">'
            f'<div class="snap-subject-card-header">'
            f'<div>'
            f'<h3 class="snap-subject-card-title">{escape(str(name))}</h3>'
            f'<p class="snap-subject-card-section">Section {escape(str(section))}</p>'
            f'</div>'
            f'<span class="snap-subject-card-code">{escape(str(code))}</span>'
            f'</div>'
            f'{stats_markup}'
            f'</article>'
        )
        st.markdown(card_html, unsafe_allow_html=True)
        if footer_callback is not None:
            footer_callback()
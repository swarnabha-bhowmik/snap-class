import streamlit as st

def footer_home():
    st.markdown("""
        <style>
            .snap-footer-bottom {
                margin-top: 3rem;
                padding: 1.25rem 1.5rem;
                border-top: 2px solid #EB459E;
                background: rgba(224, 227, 255, 0.92);
                color: #20213a;
                text-align: center;
                font-size: 0.85rem;
                line-height: 1.5;
                box-shadow: 0 -8px 24px rgba(32, 33, 58, 0.08);
            }

            .snap-footer-bottom strong {
                color: #5865F2;
                letter-spacing: 0.08em;
            }

            .snap-footer-bottom-links {
                display: flex;
                justify-content: center;
                gap: 0.7rem;
                margin-top: 0.45rem;
                color: #5865F2;
                font-size: 0.75rem;
                font-weight: 600;
                letter-spacing: 0.04em;
            }

            @media (max-width: 600px) {
                .snap-footer-bottom-links {
                    flex-wrap: wrap;
                    gap: 0.35rem 0.6rem;
                }
            }
        </style>
        <div class="snap-footer-bottom">
            <div>&copy; 2026 <strong>SNAP CLASS</strong>. All rights reserved. Crafted for smart classrooms.</div>
            <div class="snap-footer-bottom-links">
                <span>Fast Attendance</span>
                <span aria-hidden="true">&bull;</span>
                <span>Anti-Spoofing AI</span>
                <span aria-hidden="true">&bull;</span>
                <span>v1.0.0</span>
            </div>
        </div>
    """, unsafe_allow_html=True)
import streamlit as st
from typing import Any

def h1(text: str) -> None:
    """Render text as an H1 heading with brand styling."""
    st.markdown(f'<h1 style="font-family: \'Bricolage Grotesque\', sans-serif; font-size: 5.65rem;">{text}</h1>', unsafe_allow_html=True)

def h2(text: str) -> None:
    """Render text as an H2 heading with brand styling."""
    st.markdown(f'<h2 style="font-family: \'Bricolage Grotesque\', sans-serif; font-size: 4rem;">{text}</h2>', unsafe_allow_html=True)

def h3(text: str) -> None:
    """Render text as an H3 heading with brand styling."""
    st.markdown(f'<h3 style="font-family: \'Bricolage Grotesque\', sans-serif; font-size: 2rem;">{text}</h3>', unsafe_allow_html=True)

def h4(text: str) -> None:
    """Render text as an H4 heading with brand styling."""
    st.markdown(f'<h4 style="font-family: \'Bricolage Grotesque\', sans-serif; font-size: 1.41rem;">{text}</h4>', unsafe_allow_html=True)

def body(text: str) -> None:
    """Render text as body text with brand styling."""
    st.markdown(f'<p style="font-family: \'Figtree\', sans-serif; font-size: 1rem; line-height: 1.6rem;">{text}</p>', unsafe_allow_html=True)

def primary_btn(label: str, key: str = None) -> bool:
    """Render a primary button with brand styling."""
    return st.button(label, key=key, use_container_width=True, type="primary")

def card(container: "st.delta_generator.DeltaGenerator") -> None:
    """Apply card styling to a container."""
    container.markdown(
        f'<div style="background:var(--clr-fog);padding:var(--space-2x);'
        f'border-radius:var(--radius-card);box-shadow:0 4px 12px var(--charcoal-05)">',
        unsafe_allow_html=True
    ) 
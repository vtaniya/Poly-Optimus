import streamlit as st
import pandas as pd
import json
import time
import subprocess
import os
import plotly.express as px

# Setup page config
st.set_page_config(
    page_title="Poly-Optimus | LBC Benchmark Suite",
    page_icon="⚡",
    layout="wide"
)

# Custom CSS for Premium Look
st.markdown("""
<style>
    .main {
        background-color: #0e1117;
    }
    .stButton>button {
        width: 100%;
        border-radius: 10px;
        height: 3em;
        background: linear-gradient(90deg, #4b6cb7 0%, #182848 100%);
        color: white;
        font-weight: bold;
        border: none;
        transition: 0.3s;
    }
    .stButton>button:hover {
        transform: scale(1.02);
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
    }
    h1 {
        color: #f0f2f6;
        font-family: 'Outfit', sans-serif;
        text-align: center;
        background: -webkit-linear-gradient(#eee, #333);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .metric-card {
        background: rgba(255, 255, 255, 0.05);
        padding: 20px;
        border-radius: 15px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        text-align: center;
        transition: 0.3s;
    }
    .metric-card:hover {
        background: rgba(255, 255, 255, 0.08);
        border-color: #00d4ff;
    }
    .recommendation-panel {
        background: rgba(0, 212, 255, 0.1);
        padding: 15px;
        border-radius: 10px;
        border-left: 5px solid #00d4ff;
        margin-top: 10px;
    }
    .complexity-card {
        background: #1a1c24;
        padding: 20px;
        border-radius: 12px;
        border: 1px solid #333;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
    }
    .workflow-node {
        background: #262730;
        padding: 10px;
        border-radius: 8px;
        border: 1px dashed #555;
        text-align: center;
        margin: 5px 0;
    }
    .arrow {
        text-align: center;
        font-size: 20px;
        color: #00d4ff;
    }
</style>
""", unsafe_allow_html=True)

st.title("⚡ Poly-Optimus LBC Benchmark")
st.markdown("<p style='text-align: center; color: #888;'>Real-Time Performance Analysis of Lattice-Based Cryptography Polynomial Operations</p>", unsafe_allow_html=True)

# Path to files
BRIDGE_PATH = os.path.join(os.path.dirname(__file__), "..", "data_bridge.json")
BENCHMARK_SCRIPT = os.path.join(os.path.dirname(__file__), "..", "algorithms", "benchmark.py")

# Sidebar for Manual Testing
with st.sidebar:
    st.header("🔬 Manual Testing Lab")
    st.markdown("Run a bespoke benchmark with custom parameters.")
    
    custom_n = st.select_slider(
        "Select Custom Degree (N)",
        options=[64, 128, 256, 512, 1024, 2048],
        value=256
    )
    
    custom_q = st.number_input(
        "Target Prime Modulo (q)",
        min_value=2,
        value=3329,
        help="Kyber uses 3329. Large N might require a larger prime (e.g. 12289, 65537)."
    )
    
    # Intelligent Algorithm Recommendation Panel
    st.markdown("### 🤖 Intelligent Recommendation")
    if custom_n < 512:
        rec_algo = "Schoolbook"
        reasoning = "O(n²) is efficient for small constants and low degrees."
    elif 512 <= custom_n < 1024:
        rec_algo = "Karatsuba"
        reasoning = "O(n^1.58) balances recursion overhead with speed for medium degrees."
    else:
        rec_algo = "NTT"
        reasoning = "O(n log n) scales much better for large polynomial degrees common in PQC."
    
    st.markdown(f"""
    <div class="recommendation-panel">
        <b style="color: #00d4ff;">Recommended Strategy: {rec_algo}</b><br>
        <span style="font-size: 0.9em; color: #ccc;">{reasoning}</span>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    if st.button("🧪 Run Custom Benchmark Instance"):
        import random
        import sys
        sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
        from algorithms import schoolbook, karatsuba, ntt
        
        st.write(f"Testing N={custom_n}, q={custom_q}...")
        
        p1 = [random.randint(0, custom_q - 1) for _ in range(custom_n)]
        p2 = [random.randint(0, custom_q - 1) for _ in range(custom_n)]
        
        try:
            t1 = time.perf_counter_ns()
            _ = schoolbook.multiply(p1, p2, custom_q)
            d1 = (time.perf_counter_ns() - t1) / 1000.0
            
            t2 = time.perf_counter_ns()
            _ = karatsuba.multiply(p1, p2, custom_q)
            d2 = (time.perf_counter_ns() - t2) / 1000.0
            
            t3 = time.perf_counter_ns()
            _ = ntt.multiply(p1, p2, custom_q, strict=True)
            d3 = (time.perf_counter_ns() - t3) / 1000.0
            
            delta = ((d1 - d3) / d1) * 100
            st.success(f"Execution Successful!")
            
            res_df = pd.DataFrame({
                "Algorithm": ["Schoolbook", "Karatsuba", "NTT"],
                "Time (µs)": [d1, d2, d3]
            })
            
            st.markdown("### 📋 Dashboard Summary Card")
            m1, m2, m3, m4 = st.columns(4)
            m1.metric("Input Degree", f"N={custom_n}")
            m2.metric("Prime Modulus", f"q={custom_q}")
            m3.metric("Fastest Algorithm", res_df.loc[res_df['Time (µs)'].idxmin()]['Algorithm'])
            m4.metric("Execution Time", f"{res_df['Time (µs)'].min():.2f} µs")
            
            st.markdown(f"""
            <div class="recommendation-panel" style="background: rgba(0, 255, 0, 0.05); border-color: #28a745;">
                <b style="color: #28a745;">🏆 Performance Winner Analysis</b><br>
                {res_df.loc[res_df['Time (µs)'].idxmin()]['Algorithm']} achieved <b>{delta:.2f}% reduction</b> in execution time compared to Schoolbook.
            </div>
            """, unsafe_allow_html=True)
            
            fig_bar = px.bar(res_df, x="Algorithm", y="Time (µs)", color="Algorithm", template="plotly_dark")
            st.plotly_chart(fig_bar, use_container_width=True)
            
        except Exception as e:
            st.error(f"Error: {e}")

# Initialize Tabs
tab1, tab2, tab3 = st.tabs(["📊 Benchmark Race", "💡 Educational Insights", "🔬 Research Impact"])

with tab1:
    st.markdown("### 🏛️ Algorithmic Complexity Bench")
    cc1, cc2, cc3 = st.columns(3)
    with cc1:
        st.markdown('<div class="complexity-card"><h4 style="color: #ff4b4b; margin: 0;">Schoolbook</h4><p style="font-size: 0.8em; color: #888;">Approach: Brute Force</p><p style="font-size: 1.2em; font-weight: bold; color: #fff;">O(n²)</p></div>', unsafe_allow_html=True)
    with cc2:
        st.markdown('<div class="complexity-card"><h4 style="color: #ffa500; margin: 0;">Karatsuba</h4><p style="font-size: 0.8em; color: #888;">Approach: Divide & Conquer</p><p style="font-size: 1.2em; font-weight: bold; color: #fff;">O(n^1.58)</p></div>', unsafe_allow_html=True)
    with cc3:
        st.markdown('<div class="complexity-card"><h4 style="color: #00d4ff; margin: 0;">NTT</h4><p style="font-size: 0.8em; color: #888;">Approach: Transform & Conquer</p><p style="font-size: 1.2em; font-weight: bold; color: #fff;">O(n log n)</p></div>', unsafe_allow_html=True)

    with st.expander("🔗 Post-Quantum Cryptography Workflow (Educational Visualization)", expanded=True):
        st.markdown("""
        <div style="padding: 10px; background: rgba(255,255,255,0.02); border-radius: 10px;">
            <div class="workflow-node">Polynomial Inputs</div><div class="arrow">↓</div>
            <div class="workflow-node" style="border-style: solid; border-color: #00d4ff;"><b>Polynomial Multiplication Engine</b></div><div class="arrow">↓</div>
            <div style="display: flex; justify-content: space-around;">
                 <div class="workflow-node" style="width: 30%;">Schoolbook</div>
                 <div class="workflow-node" style="width: 30%;">Karatsuba</div>
                 <div class="workflow-node" style="width: 30%; border-color: #00d4ff;">NTT</div>
            </div><div class="arrow">↓</div>
            <div class="workflow-node">Result Polynomial</div><div class="arrow">↓</div>
            <div class="workflow-node">Lattice-Based Cryptography Applications</div><div class="arrow">↓</div>
            <div class="workflow-node" style="background: linear-gradient(90deg, #182848 0%, #4b6cb7 100%);">Kyber / ML-KEM Inspired Operations</div>
        </div>
        """, unsafe_allow_html=True)

    if 'process' not in st.session_state:
        st.session_state.process = None

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🚀 Run Real-Time Algorithmic Race"):
            with open(BRIDGE_PATH, "w") as f:
                json.dump([], f)
            st.session_state.process = subprocess.Popen(["python", BENCHMARK_SCRIPT])
            st.success("Benchmark Started! Monitoring performance...")

    chart_placeholder = st.empty()
    table_placeholder = st.empty()

    def load_data():
        if os.path.exists(BRIDGE_PATH):
            try:
                with open(BRIDGE_PATH, "r") as f:
                    return json.load(f)
            except:
                return []
        return []

    while True:
        data = load_data()
        if data:
            df = pd.DataFrame(data)
            df_melted = df.melt(id_vars=["N"], var_name="Algorithm", value_name="Time (µs)")
            fig = px.line(df_melted, x="N", y="Time (µs)", color="Algorithm", markers=True, line_shape="spline", title="Polynomial Multiplication Performance Race", template="plotly_dark", color_discrete_map={"Schoolbook": "#ff4b4b", "Karatsuba": "#ffa500", "NTT": "#00d4ff"})
            fig.update_layout(hovermode="x unified", font_family="Inter", title_font_size=24, xaxis=dict(tickmode='array', tickvals=[256, 512, 1024, 2048]))
            chart_placeholder.plotly_chart(fig, use_container_width=True)
            with table_placeholder.container():
                st.markdown("### 📊 Raw Laboratory Metrics")
                st.dataframe(df.style.highlight_min(axis=1, subset=["Schoolbook", "Karatsuba", "NTT"], color='#004d00'), use_container_width=True)
        
        if st.session_state.process:
            if st.session_state.process.poll() is not None:
                st.session_state.process = None
                st.info("Race Finished. All metrics captured.")
        
        time.sleep(1)
        if st.session_state.process is None and data and len(data) == 4:
            last_entry = data[-1]
            n_val, school_val, karat_val, ntt_val = last_entry["N"], last_entry["Schoolbook"], last_entry["Karatsuba"], last_entry["NTT"]
            times = {"Schoolbook": school_val, "Karatsuba": karat_val, "NTT": ntt_val}
            fastest_algo = min(times, key=times.get)
            fastest_time = times[fastest_algo]
            delta = ((school_val - fastest_time) / school_val) * 100
            comp_map = {"Schoolbook": "O(n²)", "Karatsuba": "O(n^1.58)", "NTT": "O(n log n)"}
            
            st.markdown("---")
            st.markdown(f"## 🏁 Benchmarking Race Summary (N={n_val})")
            sm1, sm2, sm3, sm4, sm5 = st.columns(5)
            sm1.metric("Current N", n_val)
            sm2.metric("Prime Modulus", "3329")
            sm3.metric("Winner", fastest_algo)
            sm4.metric("Latency", f"{fastest_time:.1f}µs")
            sm5.metric("Complexity", comp_map[fastest_algo])
            
            st.markdown(f"""
            <div class="recommendation-panel" style="background: rgba(0, 255, 0, 0.05); border-color: #28a745;">
                <b style="color: #28a745;">🏆 Performance Winner Analysis</b><br>
                {fastest_algo} achieved <b>{delta:.2f}% reduction</b> in execution time compared to Schoolbook for N={n_val}.
            </div>
            """, unsafe_allow_html=True)
            break

with tab2:
    st.markdown("### 🎓 Educational Insights")
    st.info("💡 **Why Schoolbook is slow:** O(n²) involves nested loops ($n \times n$ multiplications), making it impractical as degree $n$ grows.")
    st.warning("⚡ **Why Karatsuba reduces multiplications:** It uses a divide-and-conquer trick to replace one multiplication with several additions, reducing complexity to $O(n^{1.58})$.")
    st.success("🚀 **Why NTT is preferred:** The Number Theoretic Transform converts multiplication into point-wise multiplication (like FFT), achieving $O(n \log n)$ efficiency for large-scale PQC.")

with tab3:
    st.markdown("### 🔬 Research Impact")
    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown("**Applications:**")
        st.markdown("- Post-Quantum Cryptography\n- Signal Processing\n- High Performance Computing\n- Large Polynomial Arithmetic")
    with col_b:
        st.markdown("**Future Scope:**")
        st.markdown("- GPU Acceleration\n- Parallel NTT\n- Full ML-KEM Integration\n- Memory Optimization")

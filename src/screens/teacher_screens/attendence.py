import streamlit as st
import pandas as pd
from datetime import datetime
from src.components.header import header_teacher_dashboard
from src.components.footer import footer_home
from src.ui.base_layout import style_base_layout, style_background_dashboard
from src.database.db import get_teacher, attendence_logs

def attendence_records():
    style_base_layout()
    style_background_dashboard()
    header_teacher_dashboard()
    
    st.header("Attendence Records")
    teacher_data = st.session_state.get('teacher_data', '')
    teacher_username = teacher_data['teacher_username'] if isinstance(teacher_data, dict) else teacher_data
    records = attendence_logs(get_teacher(teacher_username))
    if not records:
        st.toast(icon="⚠️", body="Records not found")
        return
    data = []
    for r in records:
        ts = r.get('timestamps') or r.get('timestamp')
        data.append({
            "ts_group": ts.split(".")[0] if ts else None,
            "Time": datetime.fromisoformat(ts).strftime("%Y-%m-%d %I:%M %p") if ts else 'N/A',
            "Subject": r['subjects']['name'],
            "Subject Code": r['subjects']['code'],
            "is_present": bool(r.get('is_present', False)),
        })
    df = pd.DataFrame(data)

    summary = (
        df.groupby(['ts_group', 'Time', 'Subject', 'Subject Code']).aggregate(
            Present_Count = ('is_present', 'sum'),
            Total_Count = ('is_present', 'count')
        ).reset_index()
    )
    summary["Attendence Stats"] = (
        "✅" + summary['Present_Count'].astype(str) + " /" + summary['Total_Count'].astype(str) + " Students"
    )
    display_df = (summary.sort_values(by='ts_group', ascending=False)
                  [['Time', 'Subject', 'Subject Code', 'Attendence Stats']]
                  )
    st.dataframe(display_df, width='stretch', hide_index=True)

    footer_home()
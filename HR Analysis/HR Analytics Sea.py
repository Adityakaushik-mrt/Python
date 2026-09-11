import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.gridspec as gridspec
import matplotlib as mpl
from matplotlib.widgets import Button 
import squarify as sq
import seaborn as sns

#Compatibility Fix for colums
if not hasattr(cm,'get_cmap'):
    cm.get_cmap=lambda name='viridis',*args,**keargs: mpl.colormaps[name]

# Load Dataset
df=pd.read_csv(r"F:\Adi Complete Project\Updated to Github\Python\HR Analyrics.csv")

text_cols=['EducationField','Department','Gender','CF_ageband','JobRole','MaritalStatus']
# df['EducationField']=df['EducationField'].fillna('Unknown').astype(str).str.strip()
for col in ['Department','Gender','CF_ageband','JobRole','MaritalStatus']:
    if col in df.columns:
        df[col]=df[col].fillna('Unknown').astype(str).str.strip()

# Create figure and deshboard title aligned at top right
fig = plt.figure(figsize=(16,9), dpi=100)
fig.patch.set_facecolor('#f4f6f9') 
fig.suptitle("HR Analytics Dashboard", fontsize=20,color='#0D2040', fontweight="bold",x=0.08, y=1,ha='left')
# grid for 5 KPI Cards
gs_kpi=gridspec.GridSpec(1,5,left=0.04,right=0.96,top=0.90,bottom=0.82,wspace=0.15,figure=fig)
kpi_axes= [fig.add_subplot(gs_kpi[0, i]) for i in range(5)]

# Set up GridSpec for subplot (leaving space at top for title and slicers 3 rows, 2 columns)
gs_chart = gridspec.GridSpec(2,3,left=.065,top=.74,right=0.99,bottom=0.06,wspace=0.25,hspace=0.3, figure=fig)

ax1 = fig.add_subplot(gs_chart[0, 0])  # Top-Left: 
ax2 = fig.add_subplot(gs_chart[0, 1])  # Top-Middle: 
ax3 = fig.add_subplot(gs_chart[0, 2])  # Top-Right: 
ax4 = fig.add_subplot(gs_chart[1, 0])  # Bottom:-Left 
ax5 = fig.add_subplot(gs_chart[1, 1])  # Bottom: Middle
ax6 = fig.add_subplot(gs_chart[1, 2])  # Bottom : Right

# finction to draw KPI Card
def draw_kpi_card(ax, title, value, border_color="#686D08"):
    ax.clear()
    ax.set_facecolor("#39CB98")
    
    # Rounded/bordered card box
    for spine in ax.spines.values():
        spine.set_edgecolor(border_color)
        spine.set_linewidth(2)
        spine.set_visible(True)

    ax.set_xticks([])
    ax.set_yticks([])
    
    # Large primary metric value
    ax.text(0.5, 0.60, f"{value}", ha='center', va='center',
            fontsize=15, fontweight='bold', color='#102A43', transform=ax.transAxes)
    
    # KPI title/label below the metric
    ax.text(0.5, 0.25, title, ha='center', va='center',
            fontsize=12, fontweight='bold', color="#501EDC", transform=ax.transAxes)

# 1. Define your unique education categories for slicers
def update_dashboard(val):    #Callback function that filters data and redraws charts based on selection
    target=str(val).strip()
    filtered_df=df.copy if target=='All' else df[df['EducationField'] == target].copy()
    filtered_df = df[df['EducationField'] == val] if val != 'All' else df
    
    # Clear previous plot
    for ax in (ax1, ax2, ax3, ax4, ax5, ax6):
        ax.clear()
# --- Compute Dynamic KPIs ---
    total_emp = int(filtered_df['Employee_Count'].sum()) if 'Employee_Count' in filtered_df.columns else len(filtered_df)
    total_attr = int(filtered_df['CF_attritioncount'].sum()) if 'CF_attritioncount' in filtered_df.columns else 0
    attr_rate = f"{(total_attr / total_emp * 100):.2f}%" if total_emp > 0 else "0.0%"
    active_emp = total_emp - total_attr
    avg_age = int(round(filtered_df['Age'].mean())) if 'Age' in filtered_df.columns and not filtered_df['Age'].empty else 0

    # Draw KPI cards into their designated axes
    draw_kpi_card(kpi_axes[0], "Total Employee", f"{total_emp:,}")
    draw_kpi_card(kpi_axes[1], "Attrition", f"{total_attr:,}")
    draw_kpi_card(kpi_axes[2], "Attrition Rate", attr_rate)
    draw_kpi_card(kpi_axes[3], "Active Employee", f"{active_emp:,}")
    draw_kpi_card(kpi_axes[4], "Average Age", f"{avg_age}")
    
    if filtered_df.empty:
        fig.canvas.draw_idle()
        return

# 1 Attriction by Department
    data=filtered_df['Department'].value_counts()
    data=data[data>0]
    ax1.clear()
    ax1.set_frame_on(True)
    ax1.pie(
    data,
    labels=data.index,
    autopct='%1.1f%%',
    startangle=90,
    textprops={'fontsize':8,'weight':'bold'}
    )
    ax1.axis('equal')
    ax1.set_frame_on(True)
    for spine in ax1.spines.values():
        spine.set_visible(True)
    ax1.set_title('Attriction by Department',fontsize=12,fontweight='bold')
    ax1.set_xticks([])
    ax1.set_yticks([])
    ax1.tick_params(axis='y',labelsize=6)
    plt.setp(ax1.get_yticklabels(),fontsize=6,fontweight='bold')
    
    # 2 Employees By Gender Age Group
    age_gender=filtered_df.groupby(['CF_ageband','Gender'])['Employee_Count'].sum().reset_index().sort_values(by='CF_ageband',ascending=True)
    age_band=age_gender['CF_ageband'].drop_duplicates().tolist()
    sns.barplot(
        data=age_gender,
        y='Employee_Count',
        x='CF_ageband',
        hue='Gender',
        order=age_band,
        estimator=sum,
        errorbar=None,
        palette='Blues_d',
        ax=ax2
    )
    for container in ax.containers:
        ax.bar_label(
            container,
            label_type='center',
            padding=2,
            fontsize=7,
            color='black',
            fontweight='bold'
    )
    ax2.set_ylabel('Total Employee',fontsize=8,fontweight='bold')
    ax2.set_xlabel('')
    ax2.legend(title='Gender',fontsize=9,title_fontsize=10,loc='upper right')
    ax2.set_ylim(0,age_gender['Employee_Count'].max()*1.15)
    ax2.set_title('Empolyee by Gender Age Group',fontsize=14,fontweight='bold')
    ax2.tick_params(axis='x',rotation=15,labelsize=8)
    ax2.tick_params(axis='y',labelsize=8)
    ax2.set_title('Employees By Gender Age Group',fontsize=14,fontweight='bold')

    plt.setp(ax2.get_xticklabels(),fontsize=8,fontweight='bold')
    plt.setp(ax2.get_yticklabels(),fontsize=8,fontweight='bold')
    sns.despine(ax=ax,top=True,right=True)

# 3 attraction by job role
    if 'JobRole' in filtered_df.columns:
        att_data=filtered_df.groupby('JobRole')['CF_attritioncount'].sum().reset_index(name='Attrition_Count')
        att_data=att_data.sort_values(by='Attrition_Count',ascending=True)
        att_data=att_data[att_data['Attrition_Count']>0]
        if not att_data.empty:
            labels=[f'{row.JobRole}\n({int(row.Attrition_Count)})' for row in att_data.itertuples()]
            sq.plot(
                sizes=att_data['Attrition_Count'],
                label=labels,
                alpha=0.9,
                color=sns.color_palette('Set3',len(att_data)),
                text_kwargs={'fontsize':6,'fontweight':'bold','color':'black'},
                ax=ax3
            )
            ax3.set_xticks([])
            ax3.set_yticks([])
            plt.xlabel('')
            plt.ylabel('')
            plt.axis('off')
        else:
            ax3.text(5,5,'No Attrition data Available.',ha='center',va='center',fontsize=10, fontweight="bold")
        ax3.set_title('Attrition By Job Role',fontsize=14,fontweight='bold')

# 4 employee by eduction field
        if 'EducationField' in filtered_df.columns:
            edu_data=filtered_df.groupby('EducationField')['Employee_Count'].sum().reset_index().sort_values(by='Employee_Count',ascending=False) # reset index -itgives the table a default numerical index
            sns.barplot(y= 'EducationField',
                        x= 'Employee_Count' ,
                        data = edu_data,
                        hue='EducationField',
                        color="#22e9df",
                        ax=ax4)

            for container in ax4.containers:
                ax4.bar_label(container,padding=3,fontsize=8,color='black',fontweight='bold')
            ax4.set_title('Employee By Eduction Field',fontsize=14,fontweight='bold')
            ax4.set_xlabel('')
            ax4.set_ylabel('Employee Count',fontsize=8,fontweight='bold')  # use for x-axis angle deg.
            ax4.tick_params(axis='x',labelsize=8)  # use for padding and spacing
            ax4.tick_params(axis='y',labelsize=8)
            plt.setp(ax4.get_yticklabels(),fontsize=6,fontweight='bold')
            plt.setp(ax4.get_xticklabels(),fontsize=8,fontweight='bold')
            sns.despine(top=True,right=True)
# 5 employee by Marital status
    if 'MaritalStatus' in filtered_df.columns:
        marital_agg=(
            filtered_df.groupby('MaritalStatus').agg(
                Total_Employee=('Employee_Count','sum'),
                                                    attrition=('CF_attritioncount','sum'),).reset_index())
        marital_agg=marital_agg.sort_values(by='Total_Employee',ascending=False)
        marital_melted=marital_agg.melt(id_vars='MaritalStatus',
                                        value_vars=['Total_Employee','attrition'],
                                        var_name='Metric',
                                        value_name='Count',
                                        )
        sns.barplot(
            data=marital_melted,
            y='MaritalStatus',
            x='Count',
            hue='Metric',
            palette='Set2',
            ax=ax5
            )
        for container in ax5.containers:
            ax5.bar_label(container,padding=3,fontsize=8,color='black',fontweight='bold')
        ax5.set_xlim(0,800)
        ax5.set_ylabel('')
        ax5.set_title('Total Employee And Attrition By Marital Status',fontsize=10,fontweight='bold')
        ax5.set_xlabel('Employee Count', fontsize=8, fontweight='bold')
        ax5.tick_params(axis='both',labelsize=8)
        ax5.tick_params(axis='y',labelsize=6)
        plt.setp(ax5.get_yticklabels(),ha='right',fontsize=8,fontweight='bold')
        sns.despine(top=True,right=True) 
# 6. Create pivot table matrix
    matrix_data = filtered_df.pivot_table(
        index='JobRole',
        columns='JobSatisfaction',
        values='Employee_Count',
        aggfunc='sum',
        fill_value=0
    )# Add 'Total' column and sort rows by total descending
    matrix_data['Total'] = matrix_data.sum(axis=1)
    matrix_data = matrix_data.sort_values(by='Total', ascending=False)
    matrix_plot_data=matrix_data.drop(columns=['Total'])
    ax6.clear()
    #  Plot heatmap with Seaborn
    sns.heatmap(
        matrix_plot_data,
        annot=True,          # Displays the numbers inside each cell
        fmt='d',             # Formats numbers as integers (no decimals)
        cmap='Blues_r',        # Palette gradient: Blues, YlGnBu, viridis, etc.
        linewidths=0.5,      # Grid line separation between cells
        cbar=False,           # Color bar legend on the right
        ax=ax6
    )# 4. Styling
    ax6.set_title('Job Satisfaction Rating by Job Role', fontsize=11, fontweight='bold', pad=10)
    ax6.set_ylabel('')
    ax6.set_xlabel('Job Satisfaction',fontsize=11, fontweight='bold')
    ax6.tick_params(axis='y',labelsize=6)
    ax6.tick_params(axis='x',labelsize=8)
    plt.setp(ax6.get_yticklabels(),ha='right',fontsize=5)
    plt.setp(ax6.get_xticklabels(),ha='right',fontsize=8,fontweight='bold')


    fig.canvas.draw_idle()

# 7. Create interactive slicer button positioned at top right of the dashboard 
education_levels =sorted([e for e in df['EducationField'].unique()if e!='Unknown'])    # or your specific education column
num_buttons=['All']+ education_levels
# Create individual slicer buttons side-by-side
start_x=0.40      #slicer shift for right side
total_width=0.55  #slice total width
    # Calculate button widths dynamically based on the number of categories
button_width = total_width / len(num_buttons)
buttons = {}
for i, level in enumerate(num_buttons):
    ax_btn = fig.add_axes([start_x+(i * button_width),.96, button_width - 0.005, 0.035])
    # ax_btn = fig.add_axes([0.05 + (i * button_width), 0.91, button_width - 0.01, 0.04])
    btn = Button(ax_btn, str(level), color='#1f77b4', hovercolor='#2ca02c')
    btn.label.set_fontsize(6)
    btn.label.set_color('white')
    btn.label.set_fontweight('bold') 

        # Bind click event
    btn.on_clicked(lambda event, target=level: update_dashboard(target))    
    buttons[level] = btn
    # initial draw
    # refersh canvas
    # refersh canvas
update_dashboard('All')

plt.subplots_adjust(left=0.05,right=0.85,top=0.80,bottom=.08,hspace=0.4,wspace=0.4)
# plt.tight_layout()
plt.show()

from datetime import datetime
from re import U
import streamlit as st
import pandas as pd
import numpy as np

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from streamlit.hashing import UnhashableTypeError
from database import Report
from visualization import *
from AnalyseData import Analyse
import matplotlib as mpl
import matplotlib.pyplot as plt
from database import Report

#__________________________________________________PageLayoutSetup_______________________________________

st.set_page_config(page_title="Analysis of Best Selling Books",
                   page_icon=":books:",
                   layout='wide')

#________________________________________________Database Connection______________________________________

engine = create_engine('sqlite:///db.sqlite3')
Session = sessionmaker(bind=engine)
sess = Session()

#_______________________________________________Call Analyse Function From AnalyseData.py_________________

analysis = Analyse()

#_______________________________________________Sidebar Report Generation and Save Report___________________________________________________
#...conti
current_report = dict().fromkeys(
    ['title', 'desc', 'img_name', 'save_report'], "")


def generateReport():
    sidebar.header("Save Report")
    current_report['title'] = sidebar.text_input('Report Title')
    current_report['desc'] = sidebar.text_input('Report Description')
    current_report['img_name'] = sidebar.text_input('Image Name')
    current_report['save_report'] = sidebar.button("Save Report")


def save_report_form(fig):
    generateReport()
    if current_report['save_report']:
        with st.spinner("Saving Report..."):
            try:
                path = 'reports/'+current_report['img_name']+'.png'
                fig.write_image(path)
                report = Report(
                    title=current_report['title'], desc=current_report['desc'], img_name=path)
                sess.add(report)
                sess.commit()
                st.success('Report Saved')
            except Exception as e:
                st.error('Something went Wrong')
                print(e)


# ____________________________________________________HEADER____________________________________________

with st.spinner("Loading Data..."):
    st.markdown("""
        <style>
            .mainhead{
                font-family: Courgette ,Book Antiqua ;
                #letter-spacing:.1px;
                word-spacing:1px;
                color :#e67363; 
                text-shadow: 1px -1px 1px white, 1px -1px 2px white;
                font-size:40px;
            }
        </style>
    """, unsafe_allow_html=True)

    st.markdown("""
        <style>
            .detail{
                font-size:18px;
                letter-spacing:.1px;
                word-spacing:1px;
                font-family:Calibri;
                color:#74cb35;
                display:inline-block;
                }
        </style>
    """, unsafe_allow_html=True)
    
    st.markdown('<h1 class="mainhead"> Analysis of Best Selling Books </h1> <img src="" />',
                unsafe_allow_html=True)
    col1, col2 = st.beta_columns([5, 10])

    with col1:

        st.image('images/4.gif')

    with col2:

        col = st.beta_container()

        with col:
            st.markdown("""
                <style>
                    .content{
                    margin-top: 10%;
                    letter-spacing:.1px;
                    word-spacing:1px;
                    color:indianred;
                    margin-left:5%;}
                </style>
            """, unsafe_allow_html=True)

            st.markdown('<p class="content">Hey  There! <br> Welcome To My Project.This Project is all about Analyzing the Top BestSelling Books of Year 2009 to 2019.<br>We will be analyzing the Best Books on the basis of Reviews, Price, Rating, and the Author who had written it.<br>Our motive is to give you best idea about the trend going on. What people are liking and What they want to read in future. <br>One last tip, if you are on a mobile device, switch over to landscape for viewing ease. Give it a go! </p>', unsafe_allow_html=True)
            st.markdown(
                '<p class="content" style = "float:right;"> Made By Kavya Srivastava</p>', unsafe_allow_html=True)

st.markdown("")
st.markdown("___")

# ________________________________________________Data Details______________________________________________

df = pd.read_csv('dataset/bestsellers with categories.csv')

st.markdown(""" 
        <style>
            .head{
                font-family: Calibri, Book Antiqua; 
                font-size:4vh;
                padding-top:2%;
                padding-bottom:2%;
                font-weight:light;
                color:#ffc68a;
                #text-align:center;
            }
        </style>
        """, unsafe_allow_html=True)

@st.cache(suppress_st_warning=True)
def viewDataset(pathlist):
    
    with st.spinner("Loading Data..."):
        st.markdown(
            '<p class="head"> DataSet Used In This Project</p>', unsafe_allow_html=True)

        st.markdown("")
        st.dataframe(df)

        st.markdown(""" 
        <style>
            .block{
                font-family: Book Antiqua; 
                font-size:24px;
                 padding-top:11%;
                font-weight:light;
                color:lightblue;
            }
        </style>
        """, unsafe_allow_html=True)

        st.markdown('---')
        cols = st.beta_columns(4)
        cols[0].markdown(
            '<p class="block"> Number of Rows : <br> </p>', unsafe_allow_html=True)
        cols[1].markdown(f"# {df.shape[0]}")
        cols[2].markdown(
            '<p class= "block"> Number of Columns : <br></p>', unsafe_allow_html=True)
        cols[3].markdown(f"# {df.shape[1]}")
        st.markdown('---')

        st.markdown('<p class= "head"> Summary </p>', unsafe_allow_html=True)
        st.markdown("")
        st.dataframe(df.describe())
        st.markdown('---')

        types = {'object': 'Categorical',
                 'int64': 'Numerical', 'float64': 'Numerical'}
        types = list(map(lambda t: types[str(t)], df.dtypes))
        st.markdown('<p class="head">Dataset Columns</p>',
                    unsafe_allow_html=True)
        for col, t in zip(df.columns, types):
            st.markdown(f"## {col}")
            cols = st.beta_columns(4)
            cols[0].markdown('#### Unique Values :')
            cols[1].markdown(f"## {df[col].unique().size}")
            cols[2].markdown('#### Type :')
            cols[3].markdown(f"## {t}")
            st.markdown("___")


#___________________________________________________Analyze By Genre____________________________

def analyseByGenre():

    # --------------------------------------------Fiction Vs Non Fiction-------------------------------
    st.header("Analysis On the basis of Genre")
    st.markdown("")
    with st.spinner("Loading Data..."):
        #st.markdown('<h3  style = "float:right; font-family: Book Antiqua; margin:20%;"> Fiction Vs Non Fiction Books</h1> <img style ="float:left; width:35px " src="https://blogs.glowscotland.org.uk/re/public/glencoatsprimary/uploads/sites/2371/2015/11/animated-book-image-00191.gif"" />' , unsafe_allow_html=True)
        st.markdown(
            '<p class="head"> Fiction Vs Non-Fiction Books</p>', unsafe_allow_html=True)
        col1, col2 = st.beta_columns(2)
        with col1:
            data = analysis.getFicVsNonFic()
            fig = plotpie(data.index, data.values,
                          'Pie Chart of Fiction Vs Non-Fiction', "seaborn")
            st.plotly_chart(fig, use_container_width=True)
            save_this_report = st.checkbox("Save Report", key='1')
            if save_this_report:
                save_report_form(fig)
            
        with col2:
            data = analysis.getFicVsNonFic()
            fig = plotBar(data.index, data.values, "Bar Chart of Fiction Vs Non Fiction",
                          "Genre", "No Of Books", 400, 450, "ggplot2")
            st.plotly_chart(fig, use_container_width=True)
            save_this_report = st.checkbox("Save Report", key='2')
            if save_this_report:
                save_report_form(fig)

        st.markdown(
            '<p class="detail">Non-Fiction BestSellers Are More Than Fiction</p>', unsafe_allow_html=True)

    # ---------------------------------View Number of Fiction and Non FIction Books Published Per Year----------------
    
    st.markdown("___")
    with st.spinner("Loading Data..."):
        st.markdown(
            '<p class = "head">Number of Fiction and Non Fiction Books Published Per Year</p>', unsafe_allow_html=True)

        # fiction books per year
        col1, col2 = st.beta_columns(2)
        with col1:
            data = analysis.getFictionPerYear()
            fig = plotBar(data.index, data.values, "Number of Fiction Book published per Year.",
                                    "Years", 'No. of Books Published', 500, 400, "seaborn")
            st.plotly_chart(fig, use_container_width=True)
            st.markdown(
                ' <p class="detail">In 2014, Maximum Number of Fiction Books were Published.</p>', unsafe_allow_html=True)
        
            save_this_report = st.checkbox("Save Report", key='3')
            if save_this_report:
                save_report_form(fig)

        # Non fiction book per year
        with col2:
            data = analysis.getNonFictionPerYear()
            st.plotly_chart(plotBar(data.index, data.values, "Number of Non Fiction Book published per Year.",
                                    "Years", "No.of Book Published", 500, 400, "ggplot2"), use_container_width=True)
            st.markdown(
                ' <p class="detail">In 2015, Maximum Number of Non-Fiction Books were Published.</p>', unsafe_allow_html=True)
            save_this_report = st.checkbox("Save Report", key='4')
            if save_this_report:
                save_report_form(fig)

    #----------------------------------------------Comparision of Genre Over Year-------------------------------

    st.markdown("___")

    st.markdown('<p class="head">Comparision of Genre</p>',
                unsafe_allow_html=True)

    with st.spinner("Loading Data..."):

        with st.spinner("Loding..."):

            fic_data1 = analysis.getFictionPerYear()
            nonfic_data1 = analysis.getNonFictionPerYear()

            fig = plotGroupedBar([nonfic_data1, fic_data1], ['Non-Fiction Books', 'Fiction Books'],
                                           "Books Published Per Year By Genre", "Years", 'No. of Books Published')
            st.plotly_chart(fig, use_container_width=True)

            st.markdown(
                '<p class = "detail">After Comparing Fiction And Non Fiction, it \
                     concluded that Maximum Number of Books Published is From Non-Fiction Genre.</p>', unsafe_allow_html=True)
            
            save_this_report = st.checkbox("Save Report", key='5')
            if save_this_report:
                save_report_form(fig)
            st.markdown("___")

        # AVERAGE RATING BY GENRE OVER YEAR

        with st.spinner("Loading..."):

            fic_data2 = analysis.getFictionRate()
            nonfic_data2 = analysis.getNonFictionRate()
            
            fig = plotGroupedBar([nonfic_data2, fic_data2], ['Non-Fiction Books', 'Fiction Books'],
                                           "AVERAGE RATING BY GENRE OVER YEAR", "Years", 'Average Rating')
            st.plotly_chart(fig, use_container_width=True)
            st.markdown(
                '<p class = "detail">Both Fiction and Non Fiction Genre have approximately same Rating.</p>', unsafe_allow_html=True)
            save_this_report = st.checkbox("Save Report", key='6')
            if save_this_report:
                save_report_form(fig)
            st.markdown("___")

        # AVERAGE RATING BY GENER OVER YEAR

        with st.spinner("Loading..."):
            fic_data3 = analysis.getFictionReview()
            nonfic_data3 = analysis.getNonFictionReview()
            st.plotly_chart(plotGroupedBar([nonfic_data3, fic_data3], ['Non-Fiction Books', 'Fiction Books'],
                                           "Average Reviews By Gener Over Year", "Years", 'Average Review'), use_container_width=True)
            st.markdown(
                '<p class= "detail">Fiction Book Having Much Better Number of Reviews.</p>', unsafe_allow_html=True)
            save_this_report = st.checkbox("Save Report", key='7')
            if save_this_report:
                save_report_form(fig)
            st.markdown("___")

        # AVERAGE RATING BY GENER OVER YEAR

        with st.spinner("Loading Data..."):
            fic_data4 = analysis.getFictionPrice()
            nonfic_data4 = analysis.getNonFictionPrice()
            st.plotly_chart(plotGroupedBar([nonfic_data4, fic_data4], ['Non-Fiction Books', 'Fiction Books'],
                                           "Average Price By Gener Over Year", "Years", 'Average Price'), use_container_width=True)
            st.markdown(
                '<p class="detail">Non-Fiction Books Having Much Higher Average Price Than The Fiction Books</p>', unsafe_allow_html=True)
            save_this_report = st.checkbox("Save Report", key='8')
            if save_this_report:
                save_report_form(fig)
            st.markdown("___")

    sidebar.markdown("")
    sidebar.markdown("<b>Conclusion:</b>\
                        <ul>\
                        <li>Most of the BestSeller Book is Non-Fiction</li> \
                        <li>Both Genre Books have almost same rating.</li>\
                        <li>Fiction Books have most reviews so propably people want to talk about it.</li>\
                        <li>Non-Fiction Books are most expensive.</li></ul>", unsafe_allow_html=True)


# ______________________________________________________Analyze By Author__________________________________________

def analysebyAuthor():

    st.header("Analysis On the basis of The Author")
    st.markdown("")

    # -------------------------------No of Books published By Authors

    st.markdown(
        '<h1 class="head">Lets See, How many BestSeller Books are Published By The Author </h1> <img>', unsafe_allow_html=True)
    with st.spinner("Loading Data..."):
        data = analysis.getBooksByAuth()
        fig = plotBar(data.index, data.values, "Number of Book Published",
                                "Author", "No of Books", 1000, 500, "ggplot2")
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('<p class="detail"> Authors who have written more bestsellers:Jeff Kinney - 12 books, Rick Riordan, Gary Chapman and Suzanne Collins - 11 books each, American Psychological Association - 10 books, Dr. Seuss and Gallup - 9 books, Rob Elliott - 8 books,  Dav Pilkey and Stephen R. Covey - 7 books each.</p>', unsafe_allow_html=True)
        save_this_report = st.checkbox("Save Report", key='9')
        if save_this_report:
            save_report_form(fig)
    st.markdown("")
    st.markdown("___")

    # ----------------------------------Author List

    st.markdown('<h1 class="head">Select Author to know its Books Reviews Rating and Price</h1><b>',
                unsafe_allow_html=True)

    with st.spinner("Loading Data..."):

        st.markdown("#### Select Author to analyse :point_down:")

        selAuthor = st.selectbox(
            options=analysis.getAuthorList(), label=" ")

    with st.spinner("Loading Data..."):
        with st.beta_container():

            col = st.beta_columns(3)
            with col[0]:
                with st.spinner("Loading Data..."):

                            # -------------- Particular Author and its Review

                    data = analysis.getverReview(selAuthor)
                    fig = plotLine(data.index, data.values,
                                             "Reviews", "", "")
                    st.plotly_chart(fig, use_container_width=True)
                    save_this_report = st.checkbox("Save Report", key='10')
                    if save_this_report:
                        save_report_form(fig)

            with col[1]:
                with st.spinner("Loading Data..."):

                        # ----------------------Particular Name of Author and its User RAting

                    data = analysis.getverRating(selAuthor)
                    fig = plotLine(data.index, data.values,
                                             "User Rating", "", "")
                    st.plotly_chart(fig, use_container_width=True)
                    save_this_report = st.checkbox("Save Report", key='11')
                    if save_this_report:
                        save_report_form(fig)           

            with col[2]:
                with st.spinner("Loading Data..."):
                        # ----------------------Particular Name of Author and its User RAting
                    data = analysis.getverPrice(selAuthor)
                    fig =plotLine(data.index, data.values,
                                             "Price", "", "")
                    st.plotly_chart(fig, use_container_width=True)
                    save_this_report = st.checkbox("Save Report", key='12')
                    if save_this_report:
                        save_report_form(fig)                         
        st.markdown(
            '<p class= "detail">Above plots show the Review, User Rating, and Price of the Selected Author.</p>', unsafe_allow_html=True)

    # --------------------------------------Scatter Chart of Relations

    st.markdown("___")

    data = analysis.avgPrice_Ratingrelation()
    fig = plotScatter(data, x='User Rating', y='Price', color='Author',
                                title='Average Price & Average Rating Of Authors With Average Price BestSellers')
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('<p class="detail">Most of the Best SellerBooks having rating between 4.4 - 4.9 are of less than 2000 rupee.</p>', unsafe_allow_html=True)
    save_this_report = st.checkbox("Save Report", key='13')
    if save_this_report:
        save_report_form(fig)

    st.markdown("___")

    data = analysis.avgPrice_Reviewrelation()
    fig = plotScatter(data, x='User Rating', y='Reviews', color='Author',
                                title='Average Review & Average Rating Of Authors With Average Review BestSellers')
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('<p class="detail">Most of the Best SellerBook having rating between 4.4 - 4.9, have reviews less than 30k, and highest reviewed books of different rating.  </p>', unsafe_allow_html=True)
    save_this_report = st.checkbox("Save Report", key='14')
    if save_this_report:
        save_report_form(fig)

    st.markdown("___")

    data = analysis.avgindex()
    fig = plotScatter(data, x='Price', y='Reviews', color='Author',
                                title='Average Price & Average Reviews Of Authors With Year BestSellers')
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('<p class="detail">Most of the Best SellerBooks having price less than 2000 rupee have reviews between 30k.  </p>', unsafe_allow_html=True)
    save_this_report = st.checkbox("Save Report", key='15')
    if save_this_report:
        save_report_form(fig)
    
    sidebar.markdown("")
    sidebar.markdown(
        "<b>Conclusion:</b>\
            <li>Jeff Kinney has published the most no. of BestSeller Books that is 12. </li>\
            <li>Best SellerBooks are of  </li>\
                <li> Price : Less than 2000 rupee</li>\
                <li>Rating : Between 4.5 - 4.9 </li>\
                 <li>Reviews : Less than 30k</li>", unsafe_allow_html=True)


#___________________________________________Analyse By Reviews__________________________________________


def analysebyReview():

    st.header("Analysis On The Basis Of Review")

    st.markdown('<p class="head">Histogram of Reviews</p>',
                unsafe_allow_html=True)

    data = analysis.getReviewDetail()
    fig = plotHistogram(data, "No of books having same Reviews",'Review', 'No Of Books')
    st.plotly_chart(fig, use_container_width=True)

    st.markdown('<p class="detail">From Above Plot we Conclude that Most Of the BestSeller\
        Books Reviews are of range 2000 - 5990. Very Less Books have review greater that 29.99K .</p>', unsafe_allow_html=True)
    
    save_this_report = st.checkbox("Save Report", key='16')
    if save_this_report:
        save_report_form(fig)

    st.markdown("")
    st.markdown("___")

    st.markdown('<p class="head">Top Reviewed Books And Authors.</p>',
                unsafe_allow_html=True)
    col = st.beta_columns(2)
    with col[0]:
        data = analysis.viewAuthReview()
        fig = plotLine(data.index, data.values, "Top Review Author",
                                 "Author", "Review")
        st.plotly_chart(fig, use_container_width=True)
        st.markdown(
            '<p class="detail">Top Reviewed Author is "Delia Owens" with 87.841k.</p>', unsafe_allow_html=True)
        
        save_this_report = st.checkbox("Save Report", key='17')
        if save_this_report:
            save_report_form(fig)

    with col[1]:

        data = analysis.viewBookReview()
        fig = plotLine(data.index, data.values, "Top Review Book","Book Title", "Review")
        st.plotly_chart(fig, use_container_width=True)
        st.markdown(
            '<p class="detail">Top Reviewed Book is "Where the Crawdads Sing" with 87.841k.</p>', unsafe_allow_html=True)
        save_this_report = st.checkbox("Save Report", key='18')
        if save_this_report:
            save_report_form(fig)

    # --------------------------------------------------------
    st.markdown("___")

    # if st.checkbox('View By Top Review Author'):
    st.markdown('<h1 class="head">Have a look of Reviews, Rating and Price of the Books of Selected Author\
         According to its Review.</h1><img>', unsafe_allow_html=True)

    st.markdown("")
    st.markdown("")

    n = st.select_slider(options=[0, 1000, 10000, 20000, 30000, 40000, 50000,
                                  60000, 70000, 80000, 90000], label='Author having No. of Reviews')
    toprevauthor = st.selectbox(
        options=analysis.getTopReviewAuth(n), label="Select Author")

    with st.beta_container():
        col = st.beta_columns(3)

        with col[0]:
            # Particular Author and its Review
            data = analysis.getverReview(toprevauthor)
            fig = plotLine(data.index, data.values,
                                     "Reviews", "", "")
            st.plotly_chart(fig, use_container_width=True)
            save_this_report = st.checkbox("Save Report", key='19')
            if save_this_report:
                save_report_form(fig)

        with col[1]:
            # Particular Name of Author and its User RAting
            data = analysis.getverRating(toprevauthor)
            fig = plotLine(data.index, data.values,
                                     "User Rating", "", "")
            st.plotly_chart(fig, use_container_width=True)
            save_this_report = st.checkbox("Save Report", key='20')
            if save_this_report:
                save_report_form(fig)

        with col[2]:
            # Particular Name of Author and its User RAting
            data = analysis.getverPrice(toprevauthor)
            fig = plotLine(data.index, data.values,
                                     "Price", "", "")
            st.plotly_chart(fig, use_container_width=True)
            save_this_report = st.checkbox("Save Report", key='21')
            if save_this_report:
                save_report_form(fig)
    st.markdown('<p class="detail">First Select the review range, then select the author having rating of that range. Now get a look of its Books Reviews, Rating and the price. </p>', unsafe_allow_html=True)
            
    sidebar.markdown(
        "<b>Conclusion: </b> <br><br> <p>'Where the Crawdads Sing' is the Top Reviewed Book of Author 'Delia Owens' with 87.841k reviews.</p>", unsafe_allow_html=True)
    st.markdown("___")
# __________________________________________________Analysis on the basis of Price_______________________

def analyseByPrice():

    st.header("Analysis On The Basis Of Price")

# ---------------------------------------------------Histogram of Price

    with st.spinner("Loading.."):
        st.markdown('<h1 class="head">Histogram of Price.</h1><img>',
                    unsafe_allow_html=True)
        data = analysis.getprice()
        fig = plotHistogram(data, "No of books having same price",
                                      'Price', 'No Of Books')
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('<p class="detail">From Above Plot we Conclude that Most Of the BestSeller Books Price are of range 600 - 990 rupee. Very Less Books are of much high cost that is above 2500 rupee.</p>', unsafe_allow_html=True)
        save_this_report = st.checkbox("Save Report", key='22')
        if save_this_report:
            save_report_form(fig)
    
    st.markdown("___")

    st.markdown('<p class="head">Price Of the Top 5 Books</p>',unsafe_allow_html=True)
    col = st.beta_columns(2)

    with col[0]:

        with st.spinner("Loading.."):

            data = analysis.getprice2()
            fig = plotBar(data.index, data.values, "Price of Books", 'Book Title',
                                    'Price', 900, 450, "plotly_white")
            # st.dataframe(data)
            st.plotly_chart(fig, use_container_width=True)
            save_this_report = st.checkbox("Save Report", key='23')
            if save_this_report:
                save_report_form(fig)       

    with col[1]:
        with st.spinner("Loading.."):
            data = analysis.getprice2()
            fig = plotLine(data.index, data.values, "Price of Books",
                                     "Book Title", "Price", "plotly_white")
            st.plotly_chart(fig, use_container_width=True)
            save_this_report = st.checkbox("Save Report", key='24')
            if save_this_report:
                save_report_form(fig)    

    st.markdown("")
    st.markdown('<p class="detail"> Above Plots Shows the Top 5 High Priced Books.</p>',
                unsafe_allow_html=True)

    st.markdown("___")

# -------------------------------------------Scatter Chart of comparision of price and user rating
    st.markdown('<p class="head">Relation Between Price and User Rating</p>',
                unsafe_allow_html=True)
    with st.spinner("Loading.."):
        data = analysis.sctterPrice_UserRating()
        fig = plotScatter(data, x='Price', y='User Rating', color='Price',
                                    title='Relation Between Price and User Rating')
        st.plotly_chart(fig, use_container_width=True)
                                   
        st.markdown(
            '<p class="detail">Here the trend line show that as the price increases the rating\
                 of the book get decreases.</p>', unsafe_allow_html=True)
        save_this_report = st.checkbox("Save Report", key='25')
        if save_this_report:
                save_report_form(fig) 
    st.markdown("___")

    # --------------------------------------FreeBooks------------------------

    st.markdown('<p class="head">Free BestSeller Books</p>',unsafe_allow_html=True)
    cols = st.beta_columns(2)

    with cols[0]:

        data = analysis.freebooks()
        fig =plotpie(data.index, data.values,
                                'Pie Chart of No. of Free Books Published', 'plotly_white')
        st.plotly_chart(fig, use_container_width=True)
        save_this_report = st.checkbox("Save Report", key='26')
        if save_this_report:
                save_report_form(fig) 

    with cols[1]:
        data = analysis.freebooks()
        fig = plotBar(data.index, data.values, 'Bar Chart of No. of Free Book Published',
                                'Genre', 'No. of Books', 500, 450, 'ggplot2')
        st.plotly_chart(fig, use_container_width=True)
        save_this_report = st.checkbox("Save Report", key='27')
        if save_this_report:
                save_report_form(fig) 
    st.markdown(
        ' <p class = "detail">Maximum Number of Books Published Free of Cost is from Fiction Category.</p>', unsafe_allow_html=True)
    
    st.markdown("")
    st.markdown("___")
    
    st.markdown('<p class="head">Number of Free BestSeller Over the Year </p>',
                unsafe_allow_html=True)
    with st.spinner("Loading Data..."):
        
        data = analysis.freeBooksperYear()
        fig = plotBar(data.index, data.values, 'No. of Free Book Published Per Year',
                                'Year', 'Count', 700, 450, 'ggplot2')
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('<p class="detail">In 2014, maximum number of free books published.\
             But In 2012 and after 2017 No free books were there.</p>', unsafe_allow_html=True)
        save_this_report = st.checkbox("Save Report", key='28')
        if save_this_report:
                save_report_form(fig) 

    st.markdown("")
    st.markdown("___")

    st.markdown('<p class="head">Number of Free Books Published By Author.</p>',
                unsafe_allow_html=True)
    data = analysis.freeBookAuth()
    fig = plotBar(data.index, data.values, 'No. of Free Book Published By Author',
                            'Author', 'Count', 700, 450, 'ggplot2')
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('<p class="detail">Harper Lee has Published the Maximum Free BestSeller Books.</p>',
                unsafe_allow_html=True)
    save_this_report = st.checkbox("Save Report", key='29')
    if save_this_report:
                save_report_form(fig) 

    st.markdown("")
    st.markdown("___")

    st.markdown('<h1 class="head">Average Rating of Free And Paid Book Over Year</h1><img>',unsafe_allow_html=True)

    cols = st.beta_columns(2)
    with st.spinner("Loading Data..."):

        data1 = analysis.freeBookAvgRating()
        data2 = analysis.BookAvgRating()

        fig = plotMultiScatter1([{'x': data1.Year, 'y': data1['User Rating']}, {
                        'x': data2.Year, 'y': data2['User Rating']}], title='Average Rating Of Free And Paid Books Over Year',xlabel='Year',ylabel='User Rating', names=['Free Books', 'Paid Books'])
        st.plotly_chart(fig, use_container_width=True)

        st.markdown(
            '<p class="detail">Average Rating of Free Book Over Year is greater than the Paid Book.</p>', unsafe_allow_html=True)
        save_this_report = st.checkbox("Save Report", key='30')
        if save_this_report:
                save_report_form(fig) 

    st.markdown("")
    st.markdown("___")

    st.markdown('<p class="head">Average Reviews of Free And Paid Book Over Year</p>',
                unsafe_allow_html=True)
    
    data1 = analysis.freeBookAvgRating()
    data2 = analysis.BookAvgRating()

    fig = plotMultiScatter1([{'x': data1.Year, 'y': data1['Reviews']}, {
        'x': data2.Year, 'y': data2['Reviews']}], title='Average Review Of Free And Paid Books Over Year',xlabel='Year',ylabel='Reviews', names=['Free Books', 'Paid Books'])
    st.plotly_chart(fig, use_container_width=True)
   
    st.markdown(
        '<p class="detail">Free Books have higher Reviews than Paid Books Over the Year.</p>', unsafe_allow_html=True)
    
    save_this_report = st.checkbox("Save Report", key='31')
    if save_this_report:
        save_report_form(fig) 
    
    st.markdown("")
    st.markdown("___")

    cols = st.beta_columns(2)
    with cols[0]:
        with st.spinner("Loading Data..."):
            data = analysis.freeBookAvgRating()
            fig = plotScatter1(data, x='Year', y='Reviews',
                                         title='Average Review Of free Books Over Year')
            st.plotly_chart(fig, use_container_width=True)
            st.markdown(
                '<p class="detail">2017 have the maximum Average Review of Free Book</p>', unsafe_allow_html=True)
            save_this_report = st.checkbox("Save Report", key='32')
            if save_this_report:
                save_report_form(fig) 

    with cols[1]:
        with st.spinner("Loading Data..."):
            data = analysis.BookAvgRating()
            fig = plotScatter1(data, x='Year', y='Reviews',
                                         title='Average Review Of Paid Books Over Year')
            st.plotly_chart(fig, use_container_width=True)
            st.markdown(
                '<p class="detail">Maximum Average Reviews of Book Over Year is seen in 2014.</p>', unsafe_allow_html=True)
            save_this_report = st.checkbox("Save Report", key='33')
            if save_this_report:
                save_report_form(fig) 

    sidebar.markdown("")
    sidebar.markdown("<b>Conclusion: </b><br><ul><li>Maximum No. of BestSeller Book is of 600 - 990 rupee.</li> <li>Most Expensive BestSeller Book is 'Diagnostic and Statistical Manual of Mental Disorders, 5th Edition: DSM-5'</li> <li>According to analysis, books having high price is less popular as its rating decreases.</li><li>Most of the free books are of Fiction</li><li>Maximum free book is published 2014.</li><li>Harper Lee has published maximum that is 4 Free books.</li>", unsafe_allow_html=True)

    st.markdown("___")

# _________________________________________________________ANalyze By Year_______________________________


def analysebyYear():

    st.write("## Analysis on the basis of Year")
    st.markdown("")

    # ------------------------------------------Average Review Over The Year

    st.markdown('<h1 class="head">Average Review Over Year</h1><img>',
                unsafe_allow_html=True)

    col1, col2 = st.beta_columns(2)

    with col1:
        data = analysis.avgRevOverYear()
        fig = plotBar(data.index, data.values, "Bar Chart", 'Year',
                                'Average Review', 700, 450, "plotly_dark")
        st.plotly_chart(fig, use_container_width=True)
        save_this_report = st.checkbox("Save Report", key='34')
        if save_this_report:
            save_report_form(fig) 

    with col2:
        # if st.checkbox('Line Chart of Average Review Over Year'):
        data = analysis.avgRevOverYear()
        fig = plotLine(data.index, data.values,
                                 "Line Chart", "Year", "Average Review")
        st.plotly_chart(fig, use_container_width=True)
        save_this_report = st.checkbox("Save Report", key='35')
        if save_this_report:
            save_report_form(fig)                          
    st.markdown('<p class ="detail">From the above Chart we conclude that there was\
         decrement in the Average Reviews between 2014 and 2019.</p>', unsafe_allow_html=True)

    # ------------------------------------Average Price Over The Year
    st.markdown("___")

    st.markdown('<h1 class="head">Average Price Over Years</h1><img>',
                unsafe_allow_html=True)
    col3, col4 = st.beta_columns(2)

    with col3:
        # if st.checkbox('Bar Chart of Average Price Over Years'):
        data = analysis.avgPriceOverYear()
        fig = plotBar(data.index, data.values, "Bar Chart", 'Year',
                                'Average Price', 400, 450, "plotly_dark")
        st.plotly_chart(fig, use_container_width=True)
        save_this_report = st.checkbox("Save Report", key='36')
        if save_this_report:
            save_report_form(fig) 

    with col4:
        # if st.checkbox('Line Chart of Average Price Over Years'):
        data = analysis.avgPriceOverYear()
        fig  = plotLine(data.index, data.values,
                                 "Line Chart", "Year", "Price")
        st.plotly_chart(fig, use_container_width=True)
        save_this_report = st.checkbox("Save Report", key='37')
        if save_this_report:
            save_report_form(fig)

    st.markdown('<p class="detail">Average Price started reducing from 2012, suddenly in 2016 it increases\
         by 207 rupee, and then reduces over the years.</p>', unsafe_allow_html=True)

    st.markdown("___")

# -----------------------------------------Average Rating Over Years

    st.markdown('<h1 class="head">Average Rating Over Years</h1><img>',
                unsafe_allow_html=True)
    col5, col6 = st.beta_columns(2)
    with col5:
        data = analysis.avgRatingOverYear()
        fig = plotBar(data.index, data.values, "Bar Chart", 'Year',
                                'Average Rating', 700, 450, "seaborn")
        st.plotly_chart(fig, use_container_width=True)
        save_this_report = st.checkbox("Save Report", key='38')
        if save_this_report:
            save_report_form(fig)
    with col6:
        data = analysis.avgRatingOverYear()
        fig = plotLine(data.index, data.values,
                                 "Line Chart", "", "")
        st.plotly_chart(fig, use_container_width=True)
        save_this_report = st.checkbox("Save Report", key='39')
        if save_this_report:
            save_report_form(fig)
    st.markdown('<p class="detail">Average Rating Over the Years are nearly same just having a difference of\
         0.01 or 0.1 .</p>', unsafe_allow_html=True)


# ---------------------------------------------View By Years
    st.markdown("___")
    st.markdown('<h1 class="head">View By Year</h1><img>',
                unsafe_allow_html=True)
    st.markdown("Select Year to analyse :point_down:")
    with st.spinner("Loading Data..."):
        selyear = st.selectbox(
            options=analysis.getYearList(), label=" ")

        col = st.beta_columns(3)
        with col[0]:
            data = analysis.getYearReview(selyear)
            fig = plotBar(data.index, data.values, "Highest Reviewed Book of The Year",
                                    "Books", "Reviews", 1000, 700, "ggplot2")
            st.plotly_chart(fig, use_container_width=True)
            

            st.markdown(
                '<p class="detail">First Bar Specifes that this Book got the highest number of Reviews in the\
                     Selected Year</p>', unsafe_allow_html=True)
            save_this_report = st.checkbox("Save Report", key='40')
            if save_this_report:
                save_report_form(fig)  

            st.markdown("___")

        with col[1]:
            data = analysis.getYearRating(selyear)
            fig  = plotBar(data.index, data.values, "Highest Rated Book of The Year",
                                    "Books", "Rating", 1000, 700, "ggplot2")
            st.plotly_chart(fig, use_container_width=True)
            
            st.markdown(
                '<p class="detail">First Bar Specifes that this Book got the highest number of Rating in the Selected\
                     Year</p>', unsafe_allow_html=True)
            save_this_report = st.checkbox("Save Report", key='41')
            if save_this_report:
                save_report_form(fig)  

            st.markdown("___")
        with col[2]:
            data = analysis.getYearPrice(selyear)
            fig = plotBar(data.index, data.values, "Highest Price Book of The Year",
                                    "Books", "Price", 1000, 700, "ggplot2")
            st.plotly_chart(fig, use_container_width=True)
            st.markdown(
                '<p class="detail">First Bar Specifes that this Book has the highest Price in the Selected Year</p>', unsafe_allow_html=True)
            save_this_report = st.checkbox("Save Report", key='42')
            if save_this_report:
                save_report_form(fig)  

            st.markdown("___")

        st.markdown(
            '<h1 class="head">Average Price and Rating Of Top Reviewed Authors Of the Year</h1><img>', unsafe_allow_html=True)
        
        data = analysis.getYearAuthor(selyear)
        fig = plotScatter(data, x='Price', y='User Rating', color='Author',
                                    title='Average Price & Average Rating Of Top Reviewed Authors Of The Year')
        st.plotly_chart(fig, use_container_width=True)

        st.markdown('<p class="detail">The Above Scatter Chart is of The Average Price and Average Rating\
             of the Top Rated Authors Of The Selected Year. From this we come to know the relation\
              between the Authors Price and its Rating. For some author it also show the trend line ,\
                   which depicts whether its other book has growth or not in terms of price or rating.</p>', unsafe_allow_html=True)
        save_this_report = st.checkbox("Save Report", key='43')
        if save_this_report:
            save_report_form(fig)  

        st.markdown("___")

    sidebar.markdown("<b>Conclusion:</b> <li> In <b>2019</b> BestSeller Book In Terms of :</li> <li> <b>Review :</b> Where The Cowdads Sing - 87.841k </li><li> <b>Rating :</b> Oh, the Places You'll Go! - 4.9 rate </li><li> <b>Highest Price :</b> Player's Handbook(Dungeons & Dragons) - 2025 rupee <br> <b>Lowest Price :</b> The Silent Patient - 1050 rupee.</li>", unsafe_allow_html=True)


#__________________________________________________________Analyze By Rating_____________________________________

def analysebyRating():

    st.header("Analysis on The Basis of Rating")
    st.markdown('<h1 class="head">Count the average Rating</h1><img>',
                unsafe_allow_html=True)
    with st.spinner('Loading...'):
        col = st.beta_columns(2)
        with col[0]:
            data = analysis.getCountRate2()
            fig  = plotHistogram(data, "Average Rating", 'Rating',
                                          'Average No. Of Rating')
            st.plotly_chart(fig, use_container_width=True)
            save_this_report = st.checkbox("Save Report", key='44')
            if save_this_report:
                save_report_form(fig)  

        with col[1]:
            data = analysis.getCountRate()
            fig = plotBar(data.index, data.values, "Average Rating", " Rating",
                                    "Average No. of Rating", 550, 450, "ggplot2")
            st.plotly_chart(fig, use_container_width=True)
            save_this_report = st.checkbox("Save Report", key='45')
            if save_this_report:
                save_report_form(fig)                          
        st.markdown(
            '<p class="detail">MOST OF THE RATINGS ARE IN THE RANGE OF 4.6 TO 4.8</p>', unsafe_allow_html=True)

    st.markdown("___")

    st.markdown('<h1 class="head">Have a look of Reviews, Rating and Price of the Books of Selected Author According\
         to its Rating.</h1><img>', unsafe_allow_html=True)

    st.markdown("")
    st.markdown("")

    n = st.select_slider(options=[0, 5, 10],label="Select the Range of Author's Rating")

    with st.spinner('Loading...'):
        toprateauthor = st.selectbox(options=analysis.getTopRateAuth(n), label="Select Author to analyse")

    with st.beta_container():
        with st.spinner('Loading...'):

            col1, col2, col3 = st.beta_columns(3)

            with col1:
                # Particular Author and its Review
                data = analysis.getverReview(toprateauthor)
                fig = plotLine(data.index, data.values, "Reviews",
                                         "Name of The Books", "Reviews")
                st.plotly_chart(fig, use_container_width=True)
                save_this_report = st.checkbox("Save Report", key='46')
                if save_this_report:
                    save_report_form(fig)       

            with col2:
                # Particular Name of Author and its User RAting
                data = analysis.getverRating(toprateauthor)
                fig = plotLine(data.index, data.values, "User Rating",
                                         "Name of The Books", "Rating")
                st.plotly_chart(fig, use_container_width=True)
                save_this_report = st.checkbox("Save Report", key='47')
                if save_this_report:
                    save_report_form(fig)
                    
            with col3:
                # Particular Name of Author and its User RAting
                data = analysis.getverPrice(toprateauthor)
                fig = plotLine(data.index, data.values, "Price",
                                         "Name of The Books", "Price")
                st.plotly_chart(fig, use_container_width=True)
                save_this_report = st.checkbox("Save Report", key='48')
                if save_this_report:
                    save_report_form(fig)  

    st.markdown("")
    st.markdown('<p class="detail">First Select the rating range, then select the author having rating of that\
         range. Now have a look of its Books Reviews, Rating and the price. </p>', unsafe_allow_html=True)

    # -------------------------------Sidebar Conclusion

    data = analysis.AuthHighRate()
    sidebar.markdown("")
    sidebar.markdown(
        "<b>Conclusion</b>: <br> Books have rating 4.9 are of following Authors - ", unsafe_allow_html=True)
    sidebar.dataframe(data)


# ---------------------------------------------------VIew REPORT--------------------------------------------


def ViewReport():
    st.header("View Save Reports")
    reports = sess.query(Report).all()
    titleslist = [report.title for report in reports]
    selReport = st.selectbox(options=titleslist, label="Select Report")

    reportToView = sess.query(Report).filter_by(title=selReport).first()
    # st.header(reportToView.title)
    # st.text(report)

    markdown = f"""
        ### Title : {reportToView.title} 
        ###  Description :{reportToView.desc}
    """
    st.markdown(markdown)
    st.image(reportToView.img_name)


# --------------------------------------------------SIDEBAR----------------------------------

sidebar = st.sidebar
today = datetime.today()
# Textual month, day and year
d = today.strftime("%B %d, %Y %H: %M: %S")
sidebar.write(d)

sidebar.markdown("")

sidebar.markdown("""
<style> 
    .sidehead{
        float:right;
        font-family: Book Antiqua ; 
        color :Cyan; 
        margin-top:-15% !important;
    }
    .sideimg{
        width:10vh;
        float:left;
        padding-bottom:-10% !important;
        #margin-top:-50% !important;
    }
    h1{
        font-weight:light;
    }
</style>
""", unsafe_allow_html=True)

sidebar.markdown('<h1 class = "sidehead"> Analysis of Best Selling Books  </h1> <img class = "sideimg" src= "https://blogs.glowscotland.org.uk/re/public/glencoatsprimary/uploads/sites/2371/2015/11/animated-book-image-00191.gif"/>', unsafe_allow_html=True)
sidebar.markdown("### Select Your Choice :point_down:")
options = ['View Dataset', 'Analyze By Genre', 'Analyze By Price', 'Analyse By Year',
           'Analyse By Rating', 'Analyse by Reviews', 'Analyze By Author', 'View Saved Report']
choice = sidebar.selectbox(options=options, label="")
if choice == options[0]:
    viewDataset(['dataset/bestsellers with categories.csv'])
elif choice == options[1]:
    analyseByGenre()
elif choice == options[2]:
    analyseByPrice()
elif choice == options[3]:
    analysebyYear()
elif choice == options[4]:
    analysebyRating()
elif choice == options[5]:
    analysebyReview()
elif choice == options[6]:
    analysebyAuthor()
elif choice == options[7]:
    ViewReport()

#....Conti - see Above
library(tidyverse)        
library(shiny)
library(shinydashboard)
library(DT)
library(ggplot2)
library(plotly)
load("ZeGames.RData")


ui <- dashboardPage(skin = 'yellow', title = "DashBoard Games' sales and rating",
                    
                    dashboardHeader(title = "Games Popularity and Sales" ,titleWidth = 400),
                    
                    dashboardSidebar(width = 400,
                                     h1("Video Games Dashboard",style = "color:yellow;"),
                                     h4("As an avid gamer, you may be interested to find out if your favorite game is among the best rated ones or those that sold the best. The blockbuster games, are they always the best rated ones? What is the best combination of rating, genre, developer and publisher in order to have the game that will sell the best? Discover all of that and more with this Dashboard!", style = "text-align: justify; margin-left : 10px; margin-right : 15px;"),
                                     sidebarMenu(
                                       sliderInput("Years", h2("Release Year:"), min = min(ZeGames$Year_of_Release), max = max(ZeGames$Year_of_Release), value = c(1995,2005)),
                                       menuItem(h2("Developer"), tabName = "Developer", icon = icon("computer", lib = "font-awesome")),
                                       menuItem(h2("Games"), tabName = "Games", icon = icon("gamepad", lib = "font-awesome")),
                                       menuItem(h2("Sales"), tabName = "Sales", icon = icon("dollar", lib = "font-awesome")),
                                       menuItem(h2("Geography of Gaming"), tabName = "Geography", icon = icon("globe", lib = "font-awesome")),
                                       menuItem(h2("Table"), tabName = "Table", icon = icon("table", lib = "font-awesome"))
                                     )
                    ),
                    
                    dashboardBody(
                      tabItems(
                        tabItem(tabName = "Developer",
                                tabBox(
                                  title = "Developer", height = "920px", width = 12,
                                  tabPanel("General Overview",
                                           fluidRow(column(12), h1("Developer Popularity"),style="text-align: center;"),
                                           fluidRow(column(6,infoBoxOutput("box1", width = 20)),
                                                    column(6,infoBoxOutput("box2", width = 20))),
                                           fluidRow(column(12), h1("Sales"),style="text-align: center;"),
                                           fluidRow(column(6,infoBoxOutput("box3", width = 20)),
                                                    column(6,infoBoxOutput("box4", width = 20))),
                                           fluidRow(column(12), h1('Productivity'), style = "text-align: center;"),
                                           fluidRow(column(8, plotlyOutput("plot1", height = 400)),
                                                    column(4, h1("Notice"),h3("\n This general overview may be misleading. Indeed, the developers that are displayed are not the ones we expect to appear as the most successful in terms of sales, or in terms of reviews. This is why we need to apply more filters to get a more precise vision of the industry's actors"), style = "text-align: left;"))
                                  ),
                                  tabPanel("Refined Vision",
                                           fluidRow(column(6,h3("Filters")),
                                                    column(6,h3("Matching Developers"))),
                                           fluidRow(column(6,fluidRow(column(12,sliderInput("nb_games", h5("Number of Games"), min = min((ZeGames%>%group_by(Developer)%>%summarise(count = n()))$count), max = max((ZeGames%>%group_by(Developer)%>%summarise(count = n()))$count), value = median((ZeGames%>%group_by(Developer)%>%summarise(count = n()))$count)))),
                                                           fluidRow(column(12,sliderInput("total_sales", h5("Minimum Total Sales"), min = min((ZeGames%>%group_by(Developer)%>%summarise(count = sum(Global_Sales)))$count), max = max((ZeGames%>%group_by(Developer)%>%summarise(count = sum(Global_Sales)))$count), value = median((ZeGames%>%group_by(Developer)%>%summarise(count = sum(Global_Sales)))$count))))),
                                                    column(6,fluidRow(column(12,valueBoxOutput("box_dev", width = 350))),
                                                           fluidRow(column(12,valueBoxOutput("box_dev2", width = 350))))),
                                           fluidRow(column(6,h3("Top 5 Fans' Favorites")),
                                                    column(6,h3("Top 5 Critics' Choices"))),
                                           fluidRow(column(6,plotlyOutput("plot2", height = 400)),
                                                    column(6,plotlyOutput("plot3", height = 400)))
                                  ),
                                  tabPanel("Single Developer Overview",
                                           fluidRow(column(12,
                                                           selectizeInput(
                                                             inputId = "search_dev", 
                                                             label = "Search Bar",
                                                             multiple = FALSE,
                                                             choices = ZeGames$Developer,
                                                             options = list(
                                                               create = FALSE,
                                                               placeholder = "Search Me",
                                                               maxItems = '1',
                                                               onDropdownOpen = I("function($dropdown) {if (!this.lastQuery.length) {this.close(); this.settings.openOnFocus = false;}}"),
                                                               onType = I("function (str) {if (str === \"\") {this.close();}}"))))),
                                           fluidRow(column(6,h3("Platform")),
                                                    column(6,h3("Genre"))),
                                           fluidRow(column(6,plotOutput("plot4",height = 400)),
                                                    column(6,plotOutput("plot5", height = 400))),
                                           fluidRow(column(3,infoBoxOutput("box_aaa", width = 20)),
                                                    column(3,infoBoxOutput("box_aab", width = 20)),
                                                    column(3,infoBoxOutput("box_aac", width = 20)),
                                                    column(3,infoBoxOutput("box_aad", width = 20))),
                                           fluidRow(column(6,h3("Rating")),
                                                    column(6,h3("Geography of Sales"))),
                                           fluidRow(column(6,plotOutput("plot6",height = 400)),
                                                    column(6,plotOutput("plot7",height = 400)))
                                  )
                                )
                        ),
                        tabItem(tabName = "Games",
                                tabBox(
                                  title = "Games", height = "920px", width = 12,
                                  tabPanel("General Overview",
                                           fluidRow(column(6,checkboxGroupInput(
                                             "ratings",
                                             h3("Rating"),
                                             choices = unique(ZeGames$Rating),
                                             selected = NULL,
                                             inline = FALSE,
                                             width = NULL,
                                             choiceNames = NULL,
                                             choiceValues = NULL)),
                                             column(6,valueBoxOutput("rating_box", width = 350))),
                                           fluidRow(column(4,infoBoxOutput("box_ada", width = 350)),
                                                    column(4,infoBoxOutput("box_aba", width = 350)),
                                                    column(4,infoBoxOutput("box_aca", width = 350))),
                                           fluidRow(column(12,plotlyOutput("plot8", height = 400))),
                                           fluidRow(column(12,plotlyOutput("plot9", height = 400)))
                                  ),
                                  tabPanel("Single Game Overview",
                                           fluidRow(column(12,
                                                           selectizeInput(
                                                             inputId = "search_game", 
                                                             label = "Search Bar",
                                                             multiple = FALSE,
                                                             choices = ZeGames$Name,
                                                             options = list(
                                                               create = FALSE,
                                                               placeholder = "Search Me",
                                                               maxItems = '1',
                                                               onDropdownOpen = I("function($dropdown) {if (!this.lastQuery.length) {this.close(); this.settings.openOnFocus = false;}}"),
                                                               onType = I("function (str) {if (str === \"\") {this.close();}}"))))),
                                           fluidRow(column(6,h3("Geography of Sales")),
                                                    column(6,h3("Game Info"))),
                                           fluidRow(column(6,plotOutput("plot10", height = 400)),
                                                    column(6,fluidRow(column(12,valueBoxOutput("box_game1", width = 350))),
                                                           fluidRow(column(12,valueBoxOutput("box_game2", width = 350))),
                                                           fluidRow(column(12,valueBoxOutput("box_game3", width = 350))),
                                                           fluidRow(column(12,valueBoxOutput("box_game4", width = 350))))),
                                           fluidRow(column(3),
                                                    column(6,valueBoxOutput("box_game8", width = 350)),
                                                    column(3)),
                                           fluidRow(column(6,valueBoxOutput("box_game5", width = 350)),
                                                    column(6,valueBoxOutput("box_game6", width = 350))),
                                           fluidRow(column(3),
                                                    column(6,valueBoxOutput("box_game7", width = 350)),
                                                    column(3)))
                                )),
                        tabItem(tabName = "Sales",
                                tabBox(
                                  title = "Sales", height = "920px", width = 12,
                                  tabPanel("General Overview",
                                           fluidRow(column(12,plotOutput("plot_sales1",height = 600))),
                                           fluidRow(column(6,infoBoxOutput("box_sales1",width = 350)),
                                                    column(6,infoBoxOutput("box_sales2",width = 350))),
                                           fluidRow(column(12,h3("Top 5 publishers"), style="text-align: center;")),
                                           fluidRow(column(12,plotlyOutput("sales_plot", height = 400))))
                                )),
                        tabItem(tabName = "Geography",
                                tabBox(
                                  title = "Geography of Gaming", height = "920px", width = 12,
                                  tabPanel("North America",
                                           fluidRow(column(12,h3("Top 5 Genres"), style="text-align: center;")),
                                           fluidRow(column(12,plotlyOutput("local_genre1", height = 400))),
                                           fluidRow(column(12,infoBoxOutput("box_local1",width = 350)))),
                                  tabPanel("Europe",
                                           fluidRow(column(12,h3("Top 5 Genres"), style="text-align: center;")),
                                           fluidRow(column(12,plotlyOutput("local_genre2", height = 400))),
                                           fluidRow(column(12,infoBoxOutput("box_local2",width = 350))) ),
                                  tabPanel("Japan",
                                           fluidRow(column(12,h3("Top 5 Genres"), style="text-align: center;")),
                                           fluidRow(column(12,plotlyOutput("local_genre3", height = 400))),
                                           fluidRow(column(12,infoBoxOutput("box_local3",width = 350))))
                                )),
                        tabItem(tabName = "Table", 
                                dataTableOutput("table"))
                      )
                    )
)

server <- function(input, output){
  zedata <- reactive({
    ZeGames %>%
      filter(Year_of_Release >= input$Years[1],
             Year_of_Release <= input$Years[2])
  })
  zedata_2_1 <- reactive({
    zedata() %>%
      group_by(Developer)%>%
      summarise(avg_user_score = mean(User_Score),
                avg_critic_score = mean(Critic_Score))%>%
      arrange(desc(avg_critic_score))%>%
      head(1)
  })
  zedata_2_2 <- reactive({
    zedata() %>%
      group_by(Developer)%>%
      summarise(avg_user_score = mean(User_Score),
                avg_critic_score = mean(Critic_Score))%>%
      arrange(desc(avg_user_score))%>%
      head(1)
  })
  zedata_3_1 <- reactive({
    zedata() %>%
      group_by(Developer)%>%
      summarise(avg_global_sales = mean(Global_Sales))%>%
      arrange(desc(avg_global_sales))%>%
      head(1)
  })
  zedata_3_2 <- reactive({
    zedata()%>%
      filter(Developer == zedata_3_1()$Developer)%>%
      arrange(desc(Global_Sales))%>%
      head(1)
  })
  zedata_4 <- reactive({
    zedata()%>%
      group_by(Developer)%>%
      summarise(count = n(), total_sales = sum(Global_Sales))%>%
      filter(count >= input$nb_games)%>%
      filter(total_sales>= input$total_sales)
  })
  zedata_5_1 <- reactive({
    zedata()%>%
      group_by(Developer)%>%
      summarise(count = n(), total_sales = sum(Global_Sales), avg_user = mean(User_Score), avg_critic = mean(Critic_Score))%>%
      filter(count >= input$nb_games)%>%
      filter(total_sales>= input$total_sales)
  })
  zedata_6 <-reactive({
    ZeGames%>%
      filter(Developer == input$search_dev)
  })
  
  zedata_7 <- reactive({
    ZeGames%>%
      filter(Rating %in% input$ratings)
  })
  zedata_8<- reactive({
    ZeGames%>%
      filter(Name == input$search_game)
  })
  
  output$table <- renderDataTable(zedata())
  output$box1 <- renderInfoBox(
    infoBox(
      title = "Critics' Choice",
      value = zedata_2_1()$Developer,
      subtitle = paste("Score:",toString(zedata_2_1()$avg_critic_score)),
      icon = icon("pen", lib = "font-awesome"),
      color = "yellow",
      width = 6
    )
  )
  output$box2 <- renderInfoBox(
    infoBox(
      title = "Fans' Favorite",
      value = zedata_2_2()$Developer,
      subtitle =paste("Score:",toString(zedata_2_2()$avg_user_score)),
      icon = icon("user-group", lib = "font-awesome"),
      color = "yellow",
      width = 6
    )
  )
  output$box3 <- renderInfoBox(
    infoBox(
      title = "Best Selling Developer",
      value = zedata_3_1()$Developer ,
      subtitle = paste("Average Global Sales:",toString(zedata_3_1()$avg_global_sales),"Millions Units"),
      icon = icon("dollar", lib = "font-awesome"),
      color = "green",
      width = 6
    )
  )
  output$box4 <- renderInfoBox(
    infoBox(
      title = "Said Developer's best selling game",
      value = zedata_3_2()$Name,
      subtitle = paste("Global Sales:",toString(zedata_3_2()$Global_Sales),"Millions Units"),
      icon = icon("star", lib = "font-awesome"),
      color = "green",
      width = 6
    )
  )
  output$plot1<- renderPlotly({
    g_1<- zedata()%>%
      group_by(Developer)%>%
      summarise(count = n())%>%
      arrange(desc(count))%>%
      head(5)%>%
      ggplot(aes(x= reorder(Developer, count), y = count)) + geom_col(fill = "#f5d816",width = 0.4) + coord_flip() + geom_text(aes(label = count), vjust = 0) + labs(x = "Developer", y = "Number of games")
    ggplotly(g_1)
  })
  output$box_dev<-renderValueBox({
    valueBox(
      value = nrow(zedata_4()),
      subtitle = "Developers",
      icon = icon("computer", lib = "font-awesome"),
      color = "yellow"
    )
  })
  
  output$box_dev2<-renderValueBox({
    valueBox(
      value = (zedata_4()%>%arrange(desc(total_sales))%>%head(1))$Developer,
      subtitle = "Best Selling Developer",
      icon = icon("dollar", lib = "font-awesome"),
      color = "green"
    )
  })
  output$plot2 <- renderPlotly({
    g_2 <- zedata_5_1()%>%
      arrange(desc(avg_user))%>%
      head(5)%>%
      ggplot(aes(x= reorder(Developer, avg_user), y = avg_user)) + geom_col(fill = "#f5d816",width = 0.4) + coord_flip() + geom_text(aes(label = avg_user), vjust = 0) + labs(x = "Developer", y = "Fans Average Grade")
    ggplotly(g_2)
  })
  output$plot3 <- renderPlotly({
    g_3 <- zedata_5_1()%>%
      arrange(desc(avg_user))%>%
      head(5)%>%
      ggplot(aes(x= reorder(Developer, avg_critic), y = avg_critic)) + geom_col(fill = "#f5d816",width = 0.4) + coord_flip() + geom_text(aes(label = avg_critic), vjust = 0) + labs(x = "Developer", y = "Critics Average Grade")
    ggplotly(g_3)
  })
  output$plot4 <- renderPlot({
    zedata_6()%>%
      group_by(Platform)%>%
      summarise(count = n())%>%
      mutate(perc = count / sum(count)) %>%
      mutate(labels = scales::percent(perc))%>%
      ggplot(aes(x="", y=count, fill=Platform)) +
      geom_bar(stat="identity", width=1, color="white") +
      coord_polar("y", start=0) +
      geom_text(aes(label = labels),
                position = position_stack(vjust = 0.5)) + theme_void()
  })
  output$plot5 <- renderPlot({
    zedata_6()%>%
      group_by(Genre)%>%
      summarise(count = n())%>%
      mutate(perc = count / sum(count)) %>%
      mutate(labels = scales::percent(perc))%>%
      ggplot(aes(x="", y=count, fill=Genre)) +
      geom_bar(stat="identity", width=1, color="white") +
      coord_polar("y", start=0) +
      geom_text(aes(label = labels),
                position = position_stack(vjust = 0.5)) + theme_void()
  })
  output$box_aaa<- renderInfoBox({
    infoBox(
      title = "Critics' Favorite",
      value = (zedata_6()%>%arrange(desc(Critic_Score))%>%head(1))$Name,
      subtitle = paste("Score:",toString((zedata_6()%>%arrange(desc(Critic_Score))%>%head(1))$Critic_Score)),
      icon = icon("pen", lib = "font-awesome"),
      color = "yellow",
      width = 6
    )
  })
  output$box_aab<- renderInfoBox({
    infoBox(
      title = "Fans' Favorite",
      value = (zedata_6()%>%arrange(desc(User_Score))%>%head(1))$Name,
      subtitle = paste("Score:",toString((zedata_6()%>%arrange(desc(User_Score))%>%head(1))$User_Score)),
      icon = icon("user-group", lib = "font-awesome"),
      color = "yellow",
      width = 6
    )
  })
  output$box_aac<- renderInfoBox({
    infoBox(
      title = "Developer's best Selling Game",
      value = (zedata_6()%>%arrange(desc(Global_Sales))%>%head(1))$Name,
      subtitle = paste("Global Sales:",toString((zedata_6()%>%arrange(desc(Global_Sales))%>%head(1))$Global_Sales),"Millions Units"),
      icon = icon("dollar", lib = "font-awesome"),
      color = "green",
      width = 6
    )
  })
  output$box_aad <- renderInfoBox({
    infoBox(
      title = "Game's Best Region",
      value = (zedata_6()%>%arrange(desc(Global_Sales))%>%
                 head(1)%>%
                 select(NA_Sales:Other_Sales)%>%
                 rename(
                   North_America = NA_Sales,
                   Europe =EU_Sales,
                   Japan =JP_Sales,
                   Rest_of_the_world = Other_Sales)%>%
                 pivot_longer(
                   cols = North_America:Rest_of_the_world,
                   names_to = "region",
                   values_to = "Sales")%>%
                 arrange(desc(Sales))%>%
                 head(1))$region,
      subtitle = paste("Global Sales:",toString(
        (zedata_6()%>%
           arrange(desc(Global_Sales))%>%
           head(1)%>%
           select(NA_Sales:Other_Sales)%>%
           rename(
             North_America = NA_Sales,
             Europe =EU_Sales,
             Japan =JP_Sales,
             Rest_of_the_world = Other_Sales)%>%
           pivot_longer(
             cols = North_America:Rest_of_the_world,
             names_to = "region",
             values_to = "Sales")%>%
           arrange(desc(Sales))%>%
           head(1))$Sales),"Millions Units"),
      icon = icon("globe", lib = "font-awesome"),
      color = "green",
      width = 6
    )
  })
  output$plot6 <- renderPlot({
    zedata_6()%>%
      group_by(Rating)%>%
      summarise(count = n())%>%
      mutate(perc = count / sum(count)) %>%
      mutate(labels = scales::percent(perc))%>%
      ggplot(aes(x="", y=count, fill=Rating)) +
      geom_bar(stat="identity", width=1, color="white") +
      coord_polar("y", start=0) +
      geom_text(aes(label = labels),
                position = position_stack(vjust = 0.5)) + theme_void()
  })
  output$plot7<- renderPlot({
    zedata_6()%>%
      group_by(Developer)%>%
      summarise(North_America = sum(NA_Sales), Europe = sum(EU_Sales), Japan = sum(JP_Sales), Other = sum(Other_Sales))%>%
      select(North_America:Other)%>%
      pivot_longer(
        cols = North_America:Other,
        names_to = "region",
        values_to = "Sales")%>%
      mutate(perc = Sales / sum(Sales)) %>%
      mutate(labels = scales::percent(perc))%>%
      ggplot(aes(x="", y=Sales, fill=region)) +
      geom_bar(stat="identity", width=1, color="white") +
      coord_polar("y", start=0) +
      geom_text(aes(label = labels),position = position_stack(vjust = 0.5)) +
      theme_void()
  })
  output$rating_box<- renderValueBox({
    valueBox(
      value = nrow(zedata_7()%>%group_by(Name)),
      subtitle = "Games",
      icon = icon("gamepad", lib = "font-awesome"),
      color = "yellow"
    )
  })
  output$box_aba<- renderInfoBox({
    infoBox(
      title = "Fans' Favorite",
      value = (zedata_7()%>%arrange(desc(User_Score))%>%head(1))$Name,
      subtitle = paste("Score:",toString((zedata_7()%>%arrange(desc(User_Score))%>%head(1))$User_Score)),
      icon = icon("user-group", lib = "font-awesome"),
      color = "yellow",
      width = 6
    )
  })
  output$box_aca<- renderInfoBox({
    infoBox(
      title = "Critics' Choice",
      value = (zedata_7()%>%arrange(desc(Critic_Score))%>%head(1))$Name,
      subtitle = paste("Score:",toString((zedata_7()%>%arrange(desc(Critic_Score))%>%head(1))$Critic_Score)),
      icon = icon("pen", lib = "font-awesome"),
      color = "yellow",
      width = 6
    )
  })
  output$box_ada<- renderInfoBox({
    infoBox(
      title = "Best Selling Game",
      value = (zedata_7()%>%arrange(desc(Global_Sales))%>%head(1))$Name,
      subtitle = paste("Sales:",toString((zedata_7()%>%arrange(desc(Global_Sales))%>%head(1))$Global_Sales),"Millions Units"),
      icon = icon("dollar", lib = "font-awesome"),
      color = "green",
      width = 6
    )
  })
  output$plot8 <- renderPlotly({
    game_point <- zedata_7()%>%
      add_column(total_count = zedata_7()$Critic_Count + zedata_7()$User_Count)%>%
      ggplot(aes(x = total_count, y = ((User_Score*10+Critic_Score)/2), colour = Rating)) + geom_point()+ theme_light() +
      labs(x = "Total number of grade", y = "Grades (mean Users and Critics)") + geom_smooth()
    ggplotly(game_point)
  })
  
  output$plot9 <- renderPlotly({
    game_number <- zedata_7()%>%
      group_by(Year_of_Release)%>%
      summarise(count = n())%>%
      ggplot(aes(x=Year_of_Release, y= count))+geom_col(fill = 'yellow', color = "black") + theme_light() + 
      labs(x = "Year of Release", y = "Number of Games Released")
    ggplotly(game_number)
  })
  
  output$plot10<-renderPlot({
    zedata_8()%>%
      select(NA_Sales:Other_Sales)%>%
      rename(
        North_America = NA_Sales,
        Europe =EU_Sales,
        Japan =JP_Sales,
        Rest_of_the_world = Other_Sales)%>%
      pivot_longer(
        cols = North_America:Rest_of_the_world,
        names_to = "region",
        values_to = "Sales")%>%
      mutate(perc = Sales / sum(Sales)) %>%
      mutate(labels = scales::percent(perc))%>%
      ggplot(aes(x="", y=Sales, fill=region)) +
      geom_bar(stat="identity", width=1, color="white") +
      coord_polar("y", start=0) +
      geom_text(aes(label = labels),position = position_stack(vjust = 0.5)) +
      theme_void()
  })
  
  output$box_game1<-renderValueBox({
    valueBox(
      value = zedata_8()$Genre,
      subtitle = "Genre",
      icon = icon("bars", lib = "font-awesome"),
      color = "green"
    )
  })
  
  output$box_game2<-renderValueBox({
    valueBox(
      value = zedata_8()$Rating,
      subtitle = "Rating",
      icon = icon("users", lib = "font-awesome"),
      color = "green"
    )
  })
  
  output$box_game3<-renderValueBox({
    valueBox(
      value = zedata_8()$Platform,
      subtitle = "Platform",
      icon = icon("gamepad", lib = "font-awesome"),
      color = "green"
    )
  })
  
  output$box_game4<-renderValueBox({
    valueBox(
      value = zedata_8()$Developer,
      subtitle = "Best Selling Developer",
      icon = icon("computer", lib = "font-awesome"),
      color = "green"
    )
  })
  output$box_game5<-renderValueBox({
    valueBox(
      value = zedata_8()$Critic_Score,
      subtitle = "Critic Score",
      icon = icon("pen", lib = "font-awesome"),
      color = "yellow"
    )
  })
  
  output$box_game6<-renderValueBox({
    valueBox(
      value = zedata_8()$User_Score,
      subtitle = "User Score",
      icon = icon("user-group", lib = "font-awesome"),
      color = "yellow"
    )
  })
  output$box_game7<-renderValueBox({
    valueBox(
      value = (zedata_8()$User_Count + zedata_8()$Critic_Count),
      subtitle = "Amount of grades",
      icon = icon("users", lib = "font-awesome"),
      color = "yellow"
    )
  })
  output$box_game8<-renderValueBox({
    valueBox(
      value = zedata_8()$Global_Sales,
      subtitle = "Global Sales in Millions of Units",
      icon = icon("dollar", lib = "font-awesome"),
      color = "green"
    )
  })
  output$plot_sales1<- renderPlot({
    zedata()%>%
      add_column(sentiment = ((zedata()$User_Score*10 + zedata()$Critic_Score)/2))%>%
      ggplot(aes(x= sentiment, y = Global_Sales, color = Rating )) +geom_point() + 
      labs(x= "Grades", y = "Global Sales" ) + theme_minimal() + facet_grid(rows = vars(Rating), scales = "free")
  })
  output$plot_sales2<- renderPlot({
    
  })
  output$box_sales1<-renderInfoBox({
    infoBox(
      title = "Best Selling Platform",
      value = (zedata()%>% group_by(Platform)%>% summarise(somme = sum(Global_Sales))%>%arrange(desc(somme))%>%head(1))$Platform,
      subtitle = paste("Sales:",toString((zedata()%>% group_by(Platform)%>% summarise(somme = sum(Global_Sales))%>%arrange(desc(somme))%>%head(1))$somme), "Millions Units"),
      icon = icon("dollar", lib = "font-awesome"),
      color = "green",
      width = 6
    )
  })
  output$box_sales2<-renderInfoBox({
    infoBox(
      title = "Most Successful Publisher",
      value = (zedata()%>% group_by(Publisher)%>% summarise(somme = sum(Global_Sales))%>%arrange(desc(somme))%>%head(1))$Publisher,
      subtitle = paste("Sales:",toString((zedata()%>% group_by(Publisher)%>% summarise(somme = sum(Global_Sales))%>% arrange(desc(somme))%>%head(1))$somme), "Millions Units"),
      icon = icon("building", lib = "font-awesome"),
      color = "green",
      width = 6
    )
  })
  output$sales_plot<- renderPlotly({
    salesIZI<- zedata()%>%
      group_by(Publisher)%>%
      summarise(somme = sum(Global_Sales))%>%
      arrange(desc(somme))%>%
      head(5)%>%
      ggplot(aes(x= reorder(Publisher, somme), y = somme)) + geom_col(fill = "#f5d816",width = 0.4) + coord_flip() + geom_text(aes(label = somme), vjust = 0) + labs(x = "Publisher", y = "Total Global Sales")
    ggplotly(salesIZI)
  })
  output$local_genre1<- renderPlotly({
    genre1<- zedata()%>%
      group_by(Genre)%>%
      summarise(somme = sum(NA_Sales))%>%
      arrange(desc(somme))%>%
      head(5)%>%
      ggplot(aes(x= reorder(Genre, somme), y = somme)) + geom_col(fill = "#0A3161",width = 0.4) + coord_flip() + geom_text(aes(label = somme), vjust = 0) + labs(x = "Genre", y = "Total Local Sales")
    ggplotly(genre1)
  })
  output$local_genre2<- renderPlotly({
    genre2<- zedata()%>%
      group_by(Genre)%>%
      summarise(somme = sum(EU_Sales))%>%
      arrange(desc(somme))%>%
      head(5)%>%
      ggplot(aes(x= reorder(Genre, somme), y = somme)) + geom_col(fill = "#003399",width = 0.4) + coord_flip() + geom_text(aes(label = somme), vjust = 0) + labs(x = "Genre", y = "Total Local Sales")
    ggplotly(genre2)
  })
  output$local_genre3<- renderPlotly({
    genre3<- zedata()%>%
      group_by(Genre)%>%
      summarise(somme = sum(JP_Sales))%>%
      arrange(desc(somme))%>%
      head(5)%>%
      ggplot(aes(x= reorder(Genre, somme), y = somme)) + geom_col(fill = "#BC002D",width = 0.4) + coord_flip() + geom_text(aes(label = somme), vjust = 0) + labs(x = "Genre", y = "Total Local Sales")
    ggplotly(genre3)
  })
  output$box_local1<-renderInfoBox({
    infoBox(
      title = "Local Best Selling Game",
      value = (zedata()%>% arrange(desc(NA_Sales))%>%head(1))$Name,
      subtitle = paste("Sales:",toString((zedata()%>% arrange(desc(NA_Sales))%>%head(1))$NA_Sales), "Millions Units"),
      icon = icon("dollar", lib = "font-awesome"),
      color = "green",
      width = 6
    )
  })
  output$box_local2<-renderInfoBox({
    infoBox(
      title = "Local Best Selling Game",
      value = (zedata()%>% arrange(desc(EU_Sales))%>%head(1))$Name,
      subtitle = paste("Sales:",toString((zedata()%>% arrange(desc(EU_Sales))%>%head(1))$EU_Sales), "Millions Units"),
      icon = icon("dollar", lib = "font-awesome"),
      color = "green",
      width = 6
    )
  })
  output$box_local3<-renderInfoBox({
    infoBox(
      title = "Local Best Selling Game",
      value = (zedata()%>% arrange(desc(JP_Sales))%>%head(1))$Name,
      subtitle = paste("Sales:",toString((zedata()%>% arrange(desc(JP_Sales))%>%head(1))$JP_Sales), "Millions Units"),
      icon = icon("dollar", lib = "font-awesome"),
      color = "green",
      width = 6
    )
  })
}

shinyApp(ui = ui, server = server)
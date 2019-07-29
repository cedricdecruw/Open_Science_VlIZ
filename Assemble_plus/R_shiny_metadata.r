#
# This is a Shiny web application. You can run the application by clicking
# the 'Run App' button above.
#
# Find out more about building applications with Shiny here:
#
#    http://shiny.rstudio.com/
#

list.of.packages <- c("plotly", "shiny","plyr","DT","RCurl","leaflet","htmltools")
new.packages <- list.of.packages[!(list.of.packages %in% installed.packages()[,"Package"])]
if(length(new.packages)) install.packages(new.packages)

library(plotly)
library(shiny)
library(plyr)
library(DT)
require(RCurl)
library(leaflet)
library(htmltools)
# Define UI for application that draws a histogram
ui <- navbarPage("Assemble+ searcher",
                 tabPanel("Assemble+ summary viewer",
                          sidebarPanel(
                              checkboxInput("sbopt","Display options sunburst-chart:",value=TRUE),
                              conditionalPanel("input.sbopt==1",
                                               radioButtons("sboptions","Display Themes:",
                                                            c("Biology"=1,"Other"=2))
                                               ),
                              checkboxInput("dateopt","Display options date histograms:",value=TRUE),
                              conditionalPanel("input.dateopt==1",
                                               radioButtons("dateoptions","Display histogram of:",
                                                            c("begindate research"=1,"enddate research"=2,"total time research"=3))
                              ),
                              checkboxInput("geoopt","Display options map:",value=TRUE),
                              conditionalPanel("input.geoopt==1",
                                               radioButtons("spcolidse","Display collection:",
                                                            c("AssemblePlus LTER"=1,
                                                              "AssemblePlus LTERbio"=2,
                                                              "Belgian marine datasets"=3,
                                                              "EMBRC"=4)),
                                               checkboxInput("geocolor","Choose colors of markers:",value=FALSE),
                                               conditionalPanel("input.geocolor==1",
                                                                sliderInput("sizedots","Size of dots",3,5,0.05),
                                                                                 selectInput("keyword11","keyword 1:",
                                                                                             c("Benthos","Plankton","Invertebrates","Fish","Metoerology","Physical"),selected = "Benthos"),
                                                                                 selectInput("colorlterkeyword1","color keyword 1:",
                                                                                             c("yellow","red","green"),selected = "yellow"),
                                                                                 selectInput("keyword21","keyword 2:",
                                                                                             c("Benthos","Plankton","Invertebrates","Fish","Metoerology","Physical"),selected = "Benthos"),
                                                                                 selectInput("colorlterkeyword2","color keyword 2:",
                                                                                             c("yellow","red","green"),selected = "red"),
                                                                                 selectInput("keyword31","keyword 3:",
                                                                                             c("Benthos","Plankton","Invertebrates","Fish","Metoerology","Physical"),selected = "Benthos"),
                                                                                 selectInput("colorlterkeyword3","color keyword 3:",
                                                                                             c("yellow","red","green"),selected = "green")
                                                                                 
                                                                
                                                                )
                              )
                          ),
                          mainPanel(
                              tabsetPanel(
                                  tabPanel("Sunburst themes",
                                           plotlyOutput("scatMatPlot")
                                           
                                  ),
                                  tabPanel("Barplot openaccess",
                                           plotlyOutput("barplotaccess")
                                  ),
                                  tabPanel("histogram age archive/research",
                                           plotlyOutput("barplotdates")
                                  ),
                                  tabPanel("Map of documented places",
                                           leafletOutput("mymap"),
                                           DT::dataTableOutput('leaflettable')
                                  )
                              )
                          )
                          ),
                 tabPanel("archive searcher",
                            DT::dataTableOutput('ex2')
                          ),
                 tabPanel("About assemble+",
                          tags$h5("Some info about assemble+ archives etc etc lorem ipsum"))
)

# Define server logic required to draw a histogram
server <- function(input, output,session) {
    #first load in data
    con <- "S:\\datac\\Projects\\AssemblePlus\\NA2_DataAccess\\Development4AssemblePCollection\\info_metadata_Assembleplus.txt"
    rawdata <- read.csv( con, header = FALSE, sep = "|")
    #file = 'C:\\Users\\cedricd\\Documents\\Pre_upload_folder\\temp_files_screening_databases\\info_metadata.txt'
    #rawdata = read.csv(file, header = FALSE, sep = "|")
    colnames(rawdata) <- c("Themes","Themes_ID","Keywords","file_not","Link_Urls","URLIDs","DasID","Access","Surname",
                           "Firstname","Role_project","Taxterm","AphiaID","temp_start","temp_end","temp_progress",
                           "Geoterm","Measurement_parameters","Title_archive","Citations","?","Acronym institute",
                           "roleID","?","spcolname")
    
    Sys.setenv("plotly_username"="cedricd")
    Sys.setenv("plotly_api_key"="ui0LYUbveJL9u39jahNo")
    
    con <- "S:\\datac\\Projects\\AssemblePlus\\NA2_DataAccess\\Development4AssemblePCollection\\sunburst_data_Assembleplus.csv"
    d1 <- read.csv( con)
    d1 <- d1[complete.cases(d1),]
    d2 <- d1[- grep("Biology", d1$ids),]
    d2 <- d2[- grep(")", d2$ids),]
    d1 <- d1[- grep(")", d1$ids),]
    
    
    con <- "S:\\datac\\Projects\\AssemblePlus\\NA2_DataAccess\\Development4AssemblePCollection\\info_runtime_in_datasets.txt"
    datedata <- read.csv( con, header = TRUE, sep = ",")
    
    
    
    #make count of Access column for making barplot
    barplotdataacccess <- count(rawdata, vars ="Access")
    #make count of runtime variables
    begindatahistogram <- datedata$beginyear
    enddatehistogram <- datedata$endyear
    runtimehistogram <- datedata$runtime
    
    #make sunburstplot
    output$scatMatPlot <- renderPlotly({
        #all reactive variables must be present in here kut 
        if(input$sboptions == 1){sbdata <- d1}
        if(input$sboptions == 2){sbdata <- d2}
        p <- plot_ly() %>%
            add_trace(
                ids = sbdata$ids,
                labels = sbdata$label,
                parents = sbdata$parents,
                values = sbdata$values,
                type = 'sunburst',
                maxdepth = 3,
                domain = list(column = 0)
            ) %>%
            layout(
                grid = list(columns =1, rows = 1),
                margin = list(l = 0, r = 0, b = 0, t = 0),
                width = 750, height = 750,
                sunburstcolorway = c(
                    "#ffa500","#EF553B","#00cc96","#ab6305","#19d3f3",
                    "#e763fa", "#FECB52","#FFA15A","#FF6692","#B6E880"
                ),
                extendsunburstcolors = TRUE)
    })
    
#barplot with the accessrights etc
    output$barplotaccess <- renderPlotly({
        #options hier later toevoegen
        p <- plot_ly(barplotdataacccess, x = ~Access, y = ~freq, type = 'bar', name = 'SF Zoo') %>%
            layout(yaxis = list(title = 'Count'), barmode = 'group')
    })


#barplot with the runtime of years etc
    output$barplotdates <- renderPlotly({
        if(input$dateoptions == 1){
            datedat <- begindatahistogram
            gtitle <- "beginyear research"
        }
        if(input$dateoptions == 2){
            datedat <- enddatehistogram
            gtitle <- "endyear research"
        }
        if(input$dateoptions == 3){
            datedat <- runtimehistogram 
            gtitle <- "research time"
        }
        p <- plot_ly(x= datedat, type = "histogram") %>%
            layout(yaxis = list(title = '#datasets'), barmode = 'group', title = gtitle, xaxis = list(title = 'Year'))
    })
    
    
 #add data for the leaflet 
    fixData <- function(x)
    {
        x[grep('-$', x)] <- paste0('-', x[grep('-$', x)])
        x <- as.numeric(sub('-$', '', x))
        return(x)
    }
    con <- "S:\\datac\\Projects\\AssemblePlus\\NA2_DataAccess\\Development4AssemblePCollection\\info_coordinates_Assembleplus.txt"
    df <- read.csv( con, header = TRUE, sep = "!", row.names = NULL)  
    fixedData <- sapply(df[,c("lat","long")] , fixData )
    df$lat <- NULL
    df$long <- NULL
    df["lat"] <- fixedData[,1]
    df["long"] <- fixedData[,2]
    
    #merge data 
    total <- merge(rawdata,df,by="DasID")
    
 #table of data 
    output$ex2 <- DT::renderDataTable(
        #insert filter that works kut
        data <- rawdata,
        filter  ='top',
        extensions = c('Buttons','Scroller'),
        options = list(dom = 'Bfrtip',
                       autoWidth = TRUE,
                       deferRender = TRUE,
                       scrollY = 400,
                       scroller = TRUE,
                       scrollX = TRUE,
                       columnDefs = list(list(width = '5%', targets = list(2,3,4))),
            buttons = c('csv', 'excel', 'pdf', 'print',I('colvis'))
        ),
    )

    
#leaflet map 
    
    output$mymap <- renderLeaflet({
        map <- leaflet() %>%
            addProviderTiles(providers$Hydda.Base,
                             options = providerTileOptions(noWrap = TRUE)) 
        map
    })
    #make dictionary with keywords in them
    themedic <- new.env(hash = TRUE, parent=emptyenv())
    assign('Benthos', "26", themedic)
    assign('Plankton', "73", themedic)
    assign('Invertebrates', "30", themedic)
    assign('Fish', "30", themedic)
    assign('Metoerology', "40", themedic)
    assign('Physical', "55", themedic)
    #make reactive element
    observe({
        #make data selecter
        if(input$spcolidse == 1) {
            filtereddata <- total[grepl("AssemblePlus LTER", total$spcolname),]
        } else if(input$spcolidse == 2) {
            filtereddata <- total[grepl("AssemblePlus LTERbio", total$spcolname),]
        } else if(input$spcolidse == 3) {
            filtereddata <- total[grepl("Belgian marine datasets", total$spcolname),]
        }else {
            filtereddata <- total[grepl("EMBRC", total$spcolname),]
        }
        
        
        getColor <- function(filtereddata) {
            sapply(filtereddata$Themes_ID, function(Themes_ID) {
                    if(grepl(Themes_ID, themedic[[input$keyword11]])== TRUE) {
                        input$colorlterkeyword1
                    } else if(grepl(Themes_ID,themedic[[input$keyword21]])== TRUE) {
                        input$colorlterkeyword2
                    } else if(grepl(Themes_ID,themedic[[input$keyword31]])== TRUE){
                        input$colorlterkeyword3
                    }else{"white"}
                
                
            })
        }
        
        leafletProxy("mymap", data = filtereddata) %>% 
            clearShapes() %>%
            addCircles(radius =10^input$sizedots,lng = filtereddata$lat, lat = filtereddata$long, popup = as.character(filtereddata$popup), color=getColor(filtereddata))
    })
    
    
    

#leaflet info
    output$leaflettable = DT::renderDataTable({
        unique(df)
    })
}
# Run the application 
shinyApp(ui = ui, server = server)

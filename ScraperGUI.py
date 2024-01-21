
# import tkinter module
import tkinter as tk
import ScraperFormatter as sf

def add_widget_to_grid(widget,grid_row=0,grid_column=0):
    widget.grid(row = grid_row, column = grid_column, sticky = tk.W, pady = 2)
    

    
#Todo error handling
def search_jobs_button_event(event):
    
    
    positionTitle = position_title_entry.get()
    jobCategoryCode = series_entry.get()
    keyword = keyword_entry.get()
    location = location_entry.get()
    outfile_name = output_file_entry.get() 
    
    
    outfile_name += ".csv"
    
    print(jobCategoryCode,keyword,location,outfile_name)
 
    df = sf.targetted_search(positionTitle=positionTitle,jobCategoryCode=jobCategoryCode,keyword=keyword,location=location)  
    
    
    if len(df):
        df = sf.reformat_data(df)
        sf.write_job_search_to_file(df,outfile_name)
    else:
        print("No results")
    
   #  #Do not want "Anywhere in the US" or "Multiple Locations" to appear in the final results
    
   #  #df = drop_unecessary_data(df)
   #  sf.write_job_search_to_file(df,outfile_name)


    
    print("The button was clicked!")

# creating main tkinter window/toplevel
master = tk.Tk()
 
# labels describing expected input
position_title_label = tk.Label(master, text = "Position Title")
location_label = tk.Label(master, text = "Location")
job_series_label = tk.Label(master, text = "Series")
job_keyword_label = tk.Label(master, text = "Keyword")
output_file_label = tk.Label(master, text = "Output File Name")
 

# entry widgets
position_title_entry = tk.Entry(master)
location_entry = tk.Entry(master)
series_entry = tk.Entry(master)
keyword_entry = tk.Entry(master)
output_file_entry = tk.Entry(master)

position_title_entry.insert(0, "Computer Scientist") 
location_entry.insert(0, "Virginia") 
series_entry.insert(0, "1550") 
keyword_entry.insert(0, "Software Development") 
output_file_entry.insert(0, "Search Results") 

search_jobs_button = tk.Button(text="Search Jobs")
search_jobs_button.bind("<Button-1>", search_jobs_button_event)

add_widget_to_grid(position_title_label,grid_row=0,grid_column=0)
add_widget_to_grid(location_label,grid_row=1,grid_column=0)
add_widget_to_grid(job_series_label,grid_row=2,grid_column=0)
add_widget_to_grid(job_keyword_label,grid_row=3,grid_column=0)
add_widget_to_grid(output_file_label,grid_row=4,grid_column=0)
 
add_widget_to_grid(position_title_entry,grid_row=0,grid_column=1)
add_widget_to_grid(location_entry,grid_row=1,grid_column=1)
add_widget_to_grid(series_entry,grid_row=2,grid_column=1)
add_widget_to_grid(keyword_entry,grid_row=3,grid_column=1)
add_widget_to_grid(output_file_entry,grid_row=4,grid_column=1)


add_widget_to_grid(search_jobs_button,grid_row=5,grid_column=1)


 

 
# infinite loop which can be terminated by keyboard
# or mouse interrupt
tk.mainloop()
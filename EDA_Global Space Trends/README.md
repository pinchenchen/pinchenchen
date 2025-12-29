# Global Space Exploration Trends Analysis

## Overview
This project is an **Exploratory Data Analysis (EDA)** of over 60 years of space mission data. Using **R** and the **Tidyverse** visualized the history of space exploration, tracing the geopolitical shift from the Cold War-era "Space Race" to the modern rise of commercial spaceflight.

### Goals
- **Visualize** the global distribution of space launches using geospatial data.
- **Analyze** temporal trends to identify key historical eras (e.g., Cold War peak, 21st-century commercial surge).
- **Evaluate** mission success rates across different organizations and countries.

## Visualizations & Insights

### 1. Geospatial Analysis: The Global Space Map
Using the `sf` and `rnaturalearth` packages, I mapped the frequency of launches by country. This visualization highlights the dominance of traditional superpowers (USA, Russia/USSR) while revealing the emerging activity in China and Europe.

### 2. The Shift to Commercial Spaceflight
By analyzing the top launching organizations over time, the data reveals a clear transition. While state-owned entities (like NASA, RVSN USSR) dominated the 20th century, private companies (like SpaceX) have shown exponential growth in the last decade.

### 3. Temporal Trends & Success Rates
- **Volume:** The highest volume of launches occurred during the height of the Cold War.
- **Reliability:** Early space exploration (1950s-60s) had high failure rates (>40%), whereas modern missions have achieved a success rate of over 95%.

## Tech Stack & Methodology

This project relies heavily on the **R** for efficient data manipulation and high-quality visualization.

- **Data Manipulation:** `dplyr`, `janitor`, `lubridate` 
- **Visualization:** `ggplot2`
- **Geospatial:** `sf`, `rnaturalearth`

### Code Snippet: Geospatial Mapping
Here is how I merged the launch data with world geometry to create the choropleth map:

```r
# Merging space data with world map data
world_map <- ne_countries(scale = "medium", returnclass = "sf")

space_map_data <- world_map %>%
  left_join(launch_counts, by = c("name" = "Country"))

# Plotting with ggplot2 and sf
ggplot(data = space_map_data) +
  geom_sf(aes(fill = launch_count), color = "white") +
  scale_fill_viridis_c(option = "plasma", na.value = "grey90", name = "Launches") +
  labs(title = "Global Distribution of Space Launches",
       subtitle = "Number of launches by country (1957-2020)") +
  theme_minimal()
```
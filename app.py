from flask import Flask, render_template, request, jsonify
import pandas as pd
import random

app = Flask(__name__)

# Load the dataset with structured ratings
df = pd.read_csv('ratings_with_structured_reviews.csv')

# Function to get product images based on category and subcategory
def get_product_images(category, subcategory):
    # Map product to its image path (assuming images are stored in a folder /static/images/)
    image_path = f"/static/images/{category}/{subcategory}.jpg"
    return image_path

# Route to display the index page
@app.route('/')
def index():
    return render_template('index.html')

# Route to get the product details for a selected category
@app.route('/get_category', methods=['POST'])
def get_category():
    category = request.json['category']  # Get category from POST data
    
    # Get the products in the selected category
    filtered_df = df[df['category'] == category]
    
    # Get the subcategories and their details
    category_data = []
    best_product = None

    for subcategory in filtered_df['subcategory'].unique():
        subcategory_data = filtered_df[filtered_df['subcategory'] == subcategory].iloc[0]
        
        avg_rating = int(subcategory_data['rating'])  # Convert int64 to int
        total_reviews = int(subcategory_data['total_reviews'])  # Convert int64 to int
        
        product_image = get_product_images(category, subcategory)
        
        # Keep track of the best product
        if not best_product or avg_rating > best_product['avg_rating']:
            best_product = {
                'subcategory': subcategory,
                'avg_rating': avg_rating,
                'total_reviews': total_reviews,
                'product_image': product_image
            }
        
        category_data.append({
            'subcategory': subcategory,
            'avg_rating': avg_rating,
            'total_reviews': total_reviews,
            'product_image': product_image
        })
    
    # Return the category data and best product
    return jsonify({'category_data': category_data, 'best_product': best_product})

if __name__ == '__main__':
    app.run(debug=True)

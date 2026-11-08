import argparse
import requests
import json

def main(args) -> None:
    url = args.source + "/" + args.category
    response = requests.get(url, timeout=15)
    response.raise_for_status()

    products = response.json()["products"]

    results = []
    for product in products:
        results.append({
            "title": product["title"],
            "price": product["price"]
        })
    with open(args.output, "w") as fp:
        json.dump(results, fp)

def setup_arguments():
    """
    Setup arguments for the main program, including spider, max pages, and output file.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--source", 
        type=str, 
        default="https://dummyjson.com/products/category",
        help="The source of products that will be crawled.")
    parser.add_argument(
        "--category", 
        type=str, 
        default="laptops",
        help="The category of products.")
    parser.add_argument(
        "--output",
        default="products.json",
        help="path for the JSON output file (default: products.json)",
    )
    
    return parser.parse_args()

if __name__ == "__main__":
    args = setup_arguments()
    main(args)
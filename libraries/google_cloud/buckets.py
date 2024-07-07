class Buckets:
        
    # Buckets based on business country
    def get_bucket_name(business_location: str, instance: str):
        if instance in ['development','testing']:
            bucket = "europe-south-testing.softcamp.eu" # por defecto
        else:
            bucket = "europe-south-public.softcamp.eu" # por defecto

        # Mapear nombre de países para determinar una región u otra

        if business_location == 'Francia':
            bucket = "france-public.app.softcamp.eu"
        
        return bucket

    def get_bucket_url(business_location: str, public: bool, instance: str):
        bucket = Buckets.get_bucket_name(business_location, instance)

        if public:
            url_base = "https://storage.googleapis.com/"
        else:
            url_base = "https://storage.cloud.google.com/"
            
        url = url_base + bucket
        return url
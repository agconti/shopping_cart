# c
class SubdomainMiddleware:
    def process_request(self, request):
        """
        Lets store subdomains be processed naturally 
        by django url confs, by parsing the passed
        url and adding it subdomain as a property of 
        request. 
        
        Ex. guitar.store.mysite.com 

        becomes mysite.com/store_hompage/Guitar_Store
        so the store_hompage view can process it. 

        code referenced from:
        http://thingsilearned.com/2009/01/05/using-subdomains-in-django/
        """
        request.subdomain = None
        host = request.META.get('HTTP_HOST', '')
        host_s = host.replace('www.', '').split('.')
        # ensure we have a url with a subdomain 
        if len(host_s) > 2:
            request.subdomain = ' '.join(host_s[:-2])
            # get appropriate case for store titles
            request.subdomain = request.subdomain.title()
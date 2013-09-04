# c
class SubdomainMiddleware:
    def process_request(self, request):
        """
        Lets subdomains be processed naturally 
        by django url dispatcher, by parsing the passed
        url's subdomain and then adding it as a property of 
        the request. 
        
        Ex. guitar.store.mysite.com 

        stores the subdomain as "Guitar Store" in request.subdomain 
        so it can be accessed later by the project views.

        This code is referenced from:
        http://thingsilearned.com/2009/01/05/using-subdomains-in-django/
        I've customized it to suit my project needs, and while there are 
        many resources on the Internet with almost identical methods of
        doing this, I felt it was fair to give this blog poster credit.  
        """
        request.subdomain = None
        host = request.META.get('HTTP_HOST', '')
        host_s = host.replace('www.', '').split('.')
        # ensure we have a url with a subdomain 
        if len(host_s) > 2:
            request.subdomain = ' '.join(host_s[:-2])
            # get appropriate case for store titles
            request.subdomain = request.subdomain.title()
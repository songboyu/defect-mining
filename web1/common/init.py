from tornado import web


class WiseHandler(web.RequestHandler):
	@property
	def http_host(self):
		return self.request.host
	
	def compute_etag(self):
		return None
	
	def get_error_html(self, status_code, **kwargs):
		if status_code == 404:
			return self.render_string("pages-404.html")
		elif status_code == 500:
			return self.render_string("pages-500.html")
		else:
			return self.render_string("pages-500.html")


class PageNotFound(web.RequestHandler):
	def get(self):
		self.set_status(404)
		self.render("pages-404.html")
	

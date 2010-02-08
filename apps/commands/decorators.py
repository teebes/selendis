from django.utils.html import escape

def validate(method):
    """
    decorator to validate the the user is at least entering as many
    paramters as are required
    """
    
    def _validate(self, *args, **kwargs):
        template_tokens = self.template.split(' ')[1:]
        # exclude optional arguments
        required_tokens = filter(
            lambda x: x and not (x[0] == '[' and x[-1] == ']'),
            template_tokens
        )
        if len(self.tokens) < len(required_tokens):
            self.anima.notify("%s\nUsage: %s"
                              % (self.raw_cmd, self.template))
            return ['log']
        return method(self, *args, **kwargs)
    return _validate


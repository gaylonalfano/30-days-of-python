import os
import typing as t

# Look for absolute path of this file in current system
FILE_PATH = os.path.abspath(__file__)
# Find the parent directory of this file in current system
BASE_DIR = os.path.dirname(FILE_PATH)
# Set templates directory
TEMPLATE_DIR = os.path.join(BASE_DIR, "templates")


class Template:
    def __init__(
        self,
        template_name: str = "",
        context: t.Optional[t.Dict[str, str]] = None,
        *args,
        **kwargs,
    ):
        self.template_name = template_name
        self.context = context

    def get_template(self):
        template_filepath = os.path.join(TEMPLATE_DIR, self.template_name)
        # Raise exception if template_filepath doesn't exist
        if not os.path.exists(template_filepath):
            raise Exception(f"Path: -- {template_filepath} -- does not exist!")
        template_content_string: str = ""
        # Copy content inside template and save inside template_content_string
        with open(template_filepath, "r") as f:
            template_content_string = f.read()

        return template_content_string

    def render(self, context: t.Optional[t.Dict[str, str]] = None):
        """Print out the contents of the template with
        option to pass new context. The context is parsed and inserted
        into the template content placeholders.

        Params:
            context: Must convert to dict in order for string formatting.
        """
        # INSTRUCTOR:
        # render_ctx = context
        # if self.context is not None:
        #     render_ctx = self.context
        # if not isinstance(render_ctx, dict):
        #     render_ctx = {}
        # template_string = self.get_template()
        # return template_string.format(**render_ctx)

        # ATTEMPT 1:
        # render_context = context
        # print(render_context, type(render_context))
        # # Overwrite original context with new context if passed
        # if render_context is not None:
        #     self.context = render_context
        #     print(render_context, type(render_context))
        # else:
        #     # Set render_context to whatever self.context was instantiated with
        #     render_context = self.context
        #     print(render_context, type(render_context))

        # # Convert render_context to empty dict object for string formatting
        # if not isinstance(render_context, dict):
        #     render_context = {}

        # print(render_context, type(render_context))
        # # Unpack dict: {'name': 'Amy'} -> name='Amy'
        # return self.get_template().format(**render_context)

        # ATTEMPT 2:
        if context is None:
            # Set render_context to whatever self.context was instantiated with
            render_context = self.context
        else:
            # Set to new context that was passed to render
            render_context = context
        print(render_context, type(render_context))

        # Convert render_context to empty dict object for string formatting
        if not isinstance(render_context, dict):
            # render_context = {}
            # Set a default 'name' key value for string formatting or error
            render_context = {"name": "Unknown"}
        print(render_context, type(render_context))

        # Unpack dict: {'name': 'Amy'} -> name='Amy'
        return self.get_template().format(**render_context)

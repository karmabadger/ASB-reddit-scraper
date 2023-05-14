post_schema = {
    'post_id': {
        'type': 'string'
    },

    'submission_type': {
        'type': 'string',
        'required': True,
        'minlength': 1,
        # either a post or a comment
    },

    'author': {
        'type': 'string',

    },

    'upvotes': {
        'type': 'integer',
        'required': True,
    },

    'link': {
        'type': 'string',
        'required': True,
        'minlength': 1,
    }
}

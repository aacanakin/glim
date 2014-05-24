urls = {
    '/'         : 'BaseController.hello',
    '/<name>'   : 'BaseController.greet',
    '/rest'     : 'RestfulController',

    # optional restful routing with
    # 'POST /rest' : 'RestfulController',

    # route filters
    # '/' : [
    #   'BaseController.validate', # run this before the following
    #   'BaseController.greet' # and before  the following
    #   'BaseController.say_goodbye'
    # ]

    # route grouping
    # '/api' : {
    #     '/auth' : {
    #         '/me' : [
    #
    #             'BaseController'
    #         ]
    #     }
    # }
}
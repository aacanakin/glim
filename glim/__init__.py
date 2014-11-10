version = "0.8.6"

from glim import config
from glim import db
from glim import core
from glim import view
from glim import log
from glim import controller
from glim import ext
from glim import service
from glim import response

# package shortcuts for easy import
Config = config.ConfigFacade
Database = db.DatabaseFacade
Orm = db.OrmFacade
IoC = core.IoCFacade
View = view.ViewFacade
Log = log.LogFacade

Response = response.Response

Controller = controller.Controller
RestController = controller.RestController
Extension = ext.Extension
Service = service.Service

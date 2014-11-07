version = "0.8.6"

from glim import facades
from glim import core
from glim import controller
from glim import ext
from glim import service

# package shortcuts for easy import
Config = facades.Config
Database = facades.Database
Orm = facades.Orm
IoC = facades.IoC
View = facades.View
Log = facades.Log

Response = core.Response

Controller = controller.Controller
RestController = controller.RestController
Extension = ext.Extension
Service = service.Service

version = "0.9.4"

from glim import config
from glim import db
from glim import core
from glim import view
from glim import log
from glim import controller
from glim import ext
from glim import service
from glim import response
from glim import command

# package shortcuts for easy import
Config = config.ConfigFacade

Database = db.DatabaseFacade
Orm = db.OrmFacade
Model = db.Model

IoC = core.IoCFacade

View = view.ViewFacade

Log = log.LogFacade

GlimLog = log.GlimLogFacade

Command = command.Command
GlimCommand = command.GlimCommand

Response = response.Response

Controller = controller.Controller

Extension = ext.Extension

Service = service.Service

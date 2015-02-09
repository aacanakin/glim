from glim import config
from glim import core
from glim import log
from glim import controller
from glim import ext
from glim import service
from glim import response
from glim import command

# package shortcuts for easy import
Config = config.ConfigFacade

Log = log.LogFacade

GlimLog = log.GlimLogFacade

Command = command.Command
GlimCommand = command.GlimCommand

Response = response.Response
JsonResponse = response.JsonResponse

Controller = controller.Controller

Extension = ext.Extension

Service = service.Service

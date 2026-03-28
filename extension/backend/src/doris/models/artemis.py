"""Pydantic models for Artemis SVL firmware flashing."""

from pydantic import BaseModel


class SerialPortInfo(BaseModel):
    """Information about an available serial port."""

    device: str
    description: str
    hwid: str

# -*- coding: utf-8 -*-
"""
Loguru 日志工具封装类

提供统一的日志配置、文件轮转、格式化输出等功能。
"""

import os
import sys
from loguru import logger as _logger
from typing import Callable

# 移除默认的 handler，避免重复输出
_logger.remove()


class Logger:
    """
    Loguru 日志封装类（单例模式）

    使用示例::

        from log.logger import Logger

        log = Logger.setup(log_dir="logs", level="INFO")
        log.info("这是一条日志")
        log.error("发生错误: {}", e)
    """

    _instance: "Logger | None" = None
    _logger = _logger
    _is_setup = False

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    @classmethod
    def setup(
        cls,
        log_dir: str = "logs",
        app_name: str = "app",
        level: str = "INFO",
        rotation: str = "10 MB",
        retention: str = "7 days",
        format: str | None = None,
        console: bool = True,
        enqueue: bool = True,
        backtrace: bool = True,
        diagnose: bool = True,
        catch_exceptions: bool = True,
        extra: dict | None = None,
    ) -> "_logger":
        """
        配置日志（仅首次调用生效，重复调用不会重复添加 handler）

        :param log_dir: 日志文件存放目录
        :param app_name: 应用名称，用于日志文件名
        :param level: 日志级别: TRACE / DEBUG / INFO / SUCCESS / WARNING / ERROR / CRITICAL
        :param rotation: 日志轮转规则，如 "10 MB" / "00:00" / "1 week"
        :param retention: 日志保留时间，如 "7 days" / "30 days"
        :param format: 自定义日志格式，None 则使用默认格式
        :param console: 是否输出到控制台
        :param enqueue: 是否使用队列写入（多进程安全）
        :param backtrace: 是否显示完整回溯
        :param diagnose: 是否显示变量值诊断
        :param catch_exceptions: 是否捕获未处理的异常
        :param extra: 额外绑定的上下文信息
        :return: loguru.Logger 实例
        """
        if cls._is_setup:
            return cls._logger

        # 确保日志目录存在
        os.makedirs(log_dir, exist_ok=True)

        # 默认格式
        if format is None:
            format = (
                "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
                "<level>{level: <8}</level> | "
                "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | "
                "<level>{message}</level>"
            )

        # 控制台输出
        if console:
            cls._logger.add(
                sys.stdout,
                level=level,
                format=format,
                backtrace=backtrace,
                diagnose=diagnose,
                enqueue=enqueue,
                colorize=True,
            )

        # 文件输出（所有级别）
        cls._logger.add(
            os.path.join(log_dir, f"{app_name}_{{time:YYYY-MM-DD}}.log"),
            level=level,
            format=format,
            rotation=rotation,
            retention=retention,
            encoding="utf-8",
            backtrace=backtrace,
            diagnose=diagnose,
            enqueue=enqueue,
        )

        # 错误日志单独输出一份
        cls._logger.add(
            os.path.join(log_dir, f"{app_name}_error_{{time:YYYY-MM-DD}}.log"),
            level="ERROR",
            format=format,
            rotation=rotation,
            retention=retention,
            encoding="utf-8",
            backtrace=backtrace,
            diagnose=diagnose,
            enqueue=enqueue,
        )

        if extra:
            cls._logger.configure(extra=extra)

        cls._is_setup = True
        return cls._logger

    @classmethod
    def get_logger(cls) -> "_logger":
        """
        获取 logger 实例（未 setup 时自动使用默认配置）

        :return: loguru.Logger 实例
        """
        if not cls._is_setup:
            cls.setup()
        return cls._logger

    # ------------------------------------------------------------------
    # 代理到 loguru 的常用方法
    # ------------------------------------------------------------------

    def trace(self, message: str, *args, **kwargs):
        self._logger.opt(depth=1).trace(message, *args, **kwargs)

    def debug(self, message: str, *args, **kwargs):
        self._logger.opt(depth=1).debug(message, *args, **kwargs)

    def info(self, message: str, *args, **kwargs):
        self._logger.opt(depth=1).info(message, *args, **kwargs)

    def success(self, message: str, *args, **kwargs):
        self._logger.opt(depth=1).success(message, *args, **kwargs)

    def warning(self, message: str, *args, **kwargs):
        self._logger.opt(depth=1).warning(message, *args, **kwargs)

    def error(self, message: str, *args, **kwargs):
        self._logger.opt(depth=1).error(message, *args, **kwargs)

    def critical(self, message: str, *args, **kwargs):
        self._logger.opt(depth=1).critical(message, *args, **kwargs)

    def exception(self, message: str, *args, **kwargs):
        """记录异常日志，自动包含异常堆栈"""
        self._logger.opt(depth=1).exception(message, *args, **kwargs)

    # ------------------------------------------------------------------
    # 装饰器 & 上下文
    # ------------------------------------------------------------------

    @staticmethod
    def catch(
        exception: type[BaseException] = Exception,
        level: str = "ERROR",
        reraise: bool = False,
        message: str = "捕获到异常",
    ) -> Callable:
        """
        装饰器：自动捕获被装饰函数中的异常并记录日志

        :param exception: 要捕获的异常类型
        :param level: 日志级别
        :param reraise: 是否重新抛出异常
        :param message: 日志消息

        使用示例::

            @Logger.catch(ValueError, reraise=True)
            def risky_func():
                ...
        """
        return _logger.catch(
            exception=exception,
            level=level,
            reraise=reraise,
            message=message,
        )

    @staticmethod
    def contextualize(**kwargs) -> "_logger":
        """绑定上下文变量到日志中"""
        return _logger.contextualize(**kwargs)


# ------------------------------------------------------------------
# 模块级快捷接口（兼容直接调用的场景）
# ------------------------------------------------------------------

def setup_logger(**kwargs) -> "_logger":
    """快捷方法：配置并返回 logger"""
    return Logger.setup(**kwargs)


def get_logger() -> "_logger":
    """快捷方法：获取 logger 实例"""
    return Logger.get_logger()


# ------------------------------------------------------------------
# 示例
# ------------------------------------------------------------------

if __name__ == "__main__":
    # 配置日志
    log = Logger.setup(
        log_dir="logs",
        app_name="demo",
        level="DEBUG",
        rotation="5 MB",
        retention="3 days",
    )

    # 基本使用
    log.info("应用启动")
    log.debug("调试信息: {}", {"key": "value"})
    log.warning("这是一条警告")
    log.error("发生错误")
    log.success("操作成功")

    # 绑定上下文的日志
    ctx_log = Logger.contextualize(user_id="admin", request_id="req-001")
    with ctx_log:
        log.info("用户登录")  # 日志中会带上 user_id 和 request_id

    # 装饰器自动捕获异常
    @Logger.catch(message="除法计算出错")
    def divide(a, b):
        return a / b

    divide(1, 0)
import logging
import sqlite3
import threading
from sqlite3 import Error
from interface import implements
from typing import List
from liteflow.core.abstractions import IPersistenceProvider
from liteflow.core.models import WorkflowInstance, EventSubscription, Event
from .converters import *
from .tables import Tables


class SqlitePersistenceProvider(implements(IPersistenceProvider)):

    def __init__(self, database):
        if not database.endswith('.db'):
            database = f"{database}.db"
        self._connection = sqlite3.connect(database, check_same_thread=False)
        self._connection.row_factory = dict_factory
        self._cursor = self._connection.cursor()
        self._workflow_collection = self._cursor.execute(
            Tables.workflows_table)
        self._subscription_collection = self._cursor.execute(
            Tables.subscriptions_table)
        self._event_collection = self._cursor.execute(Tables.events_table)
        self.lock = threading.Lock()
        self._logger = logging.getLogger(str(self.__class__))

    def create_workflow(self, workflow: WorkflowInstance):
        self.lock.acquire()
        try:
            data = dump_workflow_instance(workflow)
            columns = ', '.join(data.keys())
            placeholders = ', '.join('?' * len(data))
            sql = f""" REPLACE INTO {Tables.workflows_table_name} ({columns}) VALUES ({placeholders})"""
            values = [int(x) if isinstance(x, bool)
                      else x for x in data.values()]
            self._cursor.execute(sql, values)
            workflow.id = str(self._cursor.lastrowid)
            self._connection.commit()
            return workflow.id
        except Error as err:
            self._logger.error(logging.exception(err))
        finally:
            self.lock.release()

    def persist_workflow(self, workflow: WorkflowInstance):
        self.lock.acquire()
        try:
            data = dump_workflow_instance(workflow)
            del data['id']
            sets = ', '.join([f"{x} = ?" for x in data.keys()])
            sql = f""" UPDATE {Tables.workflows_table_name} SET {sets} WHERE id = {workflow.id}"""
            values = [int(x) if isinstance(x, bool)
                      else x for x in data.values()]
            self._cursor.execute(sql, values)
            self._connection.commit()
        except Error as err:
            self._logger.error(logging.exception(err))
        finally:
            self.lock.release()

    def get_workflow_instance(self, id) -> WorkflowInstance:
        self.lock.acquire()
        try:
            sql = f"SELECT * FROM {Tables.workflows_table_name} where id = {id}"
            self._cursor.execute(sql)
            return load_workflow_instance(self._cursor.fetchone())
        except Error as err:
            self._logger.error(logging.exception(err))
        finally:
            self.lock.release()

    def get_runnable_instances(self) -> []:
        self.lock.acquire()
        try:
            result = []
            sql = f"SELECT id FROM {Tables.workflows_table_name} WHERE status = {WorkflowInstance.RUNNABLE}"
            self._cursor.execute(sql)
            for item in self._cursor.fetchall():
                result.append(item['id'])
            return result
        except Error as err:
            self._logger.error(logging.exception(err))
        finally:
            self.lock.release()

    def create_subscription(self, subscription: EventSubscription):
        self.lock.acquire()
        try:
            data = dump_subscription(subscription)
            columns = ', '.join(data.keys())
            placeholders = ', '.join('?' * len(data))
            sql = f""" INSERT INTO {Tables.subscriptions_table_name} ({columns}) VALUES ({placeholders})"""
            values = [int(x) if isinstance(x, bool)
                      else x for x in data.values()]
            self._cursor.execute(sql, values)
            subscription.id = str(self._cursor.lastrowid)
            self._connection.commit()
            return subscription.id
        except Error as err:
            self._logger.error(logging.exception(err))
        finally:
            self.lock.release()

    def get_subscriptions(self, event_name, event_key, effective_date) -> []:
        self.lock.acquire()
        try:
            result = []
            sql = f"SELECT * FROM {Tables.subscriptions_table_name} WHERE event_name = '{event_name}' and event_key = '{event_key}' and datetime(subscribe_as_of) <= datetime('{effective_date}')"
            self._cursor.execute(sql)
            for item in self._cursor.fetchall():
                result.append(load_subscription(item))
            return result
        except Error as err:
            self._logger.error(logging.exception(err))
        finally:
            self.lock.release()

    def terminate_subscription(self, subscription_id):
        self.lock.acquire()
        try:
            sql = f"DELETE FROM {Tables.subscriptions_table_name} where id = {subscription_id}"
            self._cursor.execute(sql)
            self._connection.commit()
        except Error as err:
            self._logger.error(logging.exception(err))
        finally:
            self.lock.release()

    def create_event(self, evt: Event):
        self.lock.acquire()
        try:
            data = dump_event(evt)
            columns = ', '.join(data.keys())
            placeholders = ', '.join('?' * len(data))
            sql = f""" INSERT INTO {Tables.events_table_name} ({columns}) VALUES ({placeholders})"""
            values = [int(x) if isinstance(x, bool)
                      else x for x in data.values()]
            self._cursor.execute(sql, values)
            evt.id = str(self._cursor.lastrowid)
            self._connection.commit()
            return evt.id
        except Error as err:
            self._logger.error(logging.exception(err))
        finally:
            self.lock.release()

    def get_event(self, event_id) -> Event:
        self.lock.acquire()
        try:
            sql = f"SELECT * FROM {Tables.events_table_name} where id = {event_id}"
            self._cursor.execute(sql)
            return load_event(self._cursor.fetchone())
        except Error as err:
            self._logger.error(logging.exception(err))
        finally:
            self.lock.release()

    def mark_event_processed(self, event_id):
        self.lock.acquire()
        try:
            sql = f"UPDATE {Tables.events_table_name} SET is_processed = 1 WHERE id = {event_id}"
            self._cursor.execute(sql)
            self._connection.commit()
        except Error as err:
            self._logger.error(logging.exception(err))
        finally:
            self.lock.release()

    def mark_event_unprocessed(self, event_id):
        self.lock.acquire()
        try:
            sql = f"UPDATE {Tables.events_table_name} SET is_processed = 0 WHERE id = {event_id}"
            self._cursor.execute(sql)
            self._connection.commit()
        except Error as err:
            self._logger.error(logging.exception(err))
        finally:
            self.lock.release()

    def get_runnable_events(self, effective_date) -> []:
        self.lock.acquire()
        try:
            result = []
            sql = f"SELECT * FROM {Tables.events_table_name} WHERE is_processed = 0 and datetime(event_time) <= datetime('{effective_date}')"
            self._cursor.execute(sql)
            for item in self._cursor.fetchall():
                result.append(item['id'])
        except Error as err:
            self._logger.error(logging.exception(err))
        finally:
            self.lock.release()
        return result

    def get_events(self, event_name, event_key, effective_date) -> []:
        self.lock.acquire()
        try:
            result = []
            sql = f"SELECT * FROM {Tables.events_table_name} WHERE event_name = '{event_name}' and event_key = '{event_key}' and datetime(event_time) >= datetime('{effective_date}')"
            self._cursor.execute(sql)
            for item in self._cursor.fetchall():
                result.append(item['id'])
        except Error as err:
            self._logger.error(logging.exception(err))
        finally:
            self.lock.release()
        return result

    def persist_errors(self, errors: []):
        pass

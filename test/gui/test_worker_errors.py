"""Tests for worker error signal propagation and QThread lifecycle after errors."""

import pytest
from PyQt6.QtCore import QThread, pyqtSignal, QObject
from PyQt6.QtTest import QSignalSpy
from PyQt6.QtWidgets import QApplication


class ErrorProneWorker(QObject):
    """Worker that can emit error signals."""
    finished = pyqtSignal()
    error = pyqtSignal(str)
    
    def __init__(self, should_error: bool = False):
        super().__init__()
        self.should_error = should_error
        self.run_called = False
        self.error_emitted = False
    
    def run(self):
        self.run_called = True
        if self.should_error:
            self.error.emit("Something went wrong")
            self.error_emitted = True
        self.finished.emit()


def wait_for_thread(thread: QThread, finished_spy: QSignalSpy, timeout: int = 500) -> None:
    """Process the queued finished signal before blocking on the thread."""
    signal_received = len(finished_spy) > 0 or finished_spy.wait(timeout)
    if signal_received:
        thread.quit()
    stopped = signal_received and thread.wait(timeout)
    if not stopped:
        thread.quit()
        stopped = thread.wait(timeout)
    assert signal_received
    assert stopped


@pytest.fixture
def qapp():
    """Create QApplication for tests."""
    app = QApplication.instance()
    if app is None:
        app = QApplication([])
    yield app


def test_worker_emits_error_signal(qapp):
    """Verify worker can emit error signal."""
    worker = ErrorProneWorker(should_error=True)
    thread = QThread()
    worker.moveToThread(thread)
    
    # Connect signals
    worker.finished.connect(thread.quit)
    thread.started.connect(worker.run)
    
    # Capture error
    error_received = []
    worker.error.connect(lambda msg: error_received.append(msg))
    finished_spy = QSignalSpy(worker.finished)
    
    thread.start()
    wait_for_thread(thread, finished_spy)
    
    assert worker.error_emitted
    assert len(error_received) == 1
    assert error_received[0] == "Something went wrong"


def test_thread_quits_after_worker_error(qapp):
    """Verify thread exits cleanly even after worker error."""
    worker = ErrorProneWorker(should_error=True)
    thread = QThread()
    worker.moveToThread(thread)
    
    worker.finished.connect(thread.quit)
    thread.started.connect(worker.run)
    finished_spy = QSignalSpy(worker.finished)
    
    thread.start()
    wait_for_thread(thread, finished_spy)
    
    # Thread should not be running
    assert not thread.isRunning()
    # Worker should have run
    assert worker.run_called


def test_worker_without_error(qapp):
    """Verify worker without error completes normally."""
    worker = ErrorProneWorker(should_error=False)
    thread = QThread()
    worker.moveToThread(thread)
    
    worker.finished.connect(thread.quit)
    thread.started.connect(worker.run)
    finished_spy = QSignalSpy(worker.finished)
    
    thread.start()
    wait_for_thread(thread, finished_spy)
    
    # Thread should not be running
    assert not thread.isRunning()
    # Worker should have run
    assert worker.run_called
    # Error should not have been emitted
    assert not worker.error_emitted


def test_multiple_errors_propagated(qapp):
    """Verify multiple errors can be emitted and propagated."""
    worker = ErrorProneWorker(should_error=False)
    thread = QThread()
    worker.moveToThread(thread)
    
    worker.finished.connect(thread.quit)
    thread.started.connect(worker.run)
    
    errors = []
    worker.error.connect(lambda msg: errors.append(msg))
    finished_spy = QSignalSpy(worker.finished)
    
    # Manually emit multiple errors before running
    worker.error.emit("Error 1")
    worker.error.emit("Error 2")
    
    thread.start()
    wait_for_thread(thread, finished_spy)
    
    # Process events to deliver signals
    QApplication.processEvents()
    
    assert len(errors) >= 2
